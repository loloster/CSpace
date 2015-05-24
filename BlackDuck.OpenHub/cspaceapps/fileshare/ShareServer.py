#!/usr/bin/env python
# CSpace ApplicationConnection Test

from cspaceapps.appletutil import ApplicationConnection, CSpaceEnv, initializeLogFile
from nitro.selectreactor import SelectReactor
from cspace.main.service import getPIDpath
from cspace.util.rpc import RPCConnection, RPCSwitchboard
from cspaceapps.filetransfer.fileserver import FileServer, SimpleFS
from cspaceapps.filetransfer.fileclient import FileClient, FileFetcher
import cspace.ext.storefwd
from HTTPServer import SimpleHTTPServer, HTTPRequestHandler


import webbrowser
import os, logging
import urlparse, os.path, posixpath, urllib, cgi
import time, socket, mimetypes

logger = logging.getLogger()

def setEnviron():
    pidfile = "CSpace.run"
    pidpath = os.path.join("~", ".CSpace")
    pidpath = os.path.expanduser(pidpath)
    pidpath = os.path.join(pidpath, pidfile)
    pidfile = file(pidpath, "rb")
    pid = pidfile.readline().strip()
    xmlrpc = pidfile.readline().strip()
    appletport = pidfile.readline().strip()
    pidfile.close()
    
    os.environ['CSPACE_PORT'] = appletport
    os.environ['CSPACE_USER'] = "cptnahab"
    os.environ['CSPACE_EVENT'] = "CONTACTACTION"
    os.environ['CSPACE_CONTACTNAME'] = "adamsmith"
    os.environ['CSPACE_ACTION'] = "Browse Shared Files..."
    os.environ['CSPACE_ACTIONDIR'] = "ShareFiles"

class ShareService:
    def __init__(self):
        self.reactor = SelectReactor()
        self.env = CSpaceEnv()
        self.conn = ApplicationConnection(self.env, self.reactor, self.startChain, self.onError)
        
    def run(self):
        self.reactor.run()
        
    def onError(self, msg):
        print "ERROR: %s" % msg
        self.shutdown()
        
    def shutdown(self):
        print "Shutting down..."
        if self.conn:
            conn = self.conn
            self.conn = None
            conn.close()
        self.reactor.stop()
        
    def startChain(self, result):
        chain = [
            ("GetMyPubKey", (), self.onMyPubKey),
            ("GetMyPrivKey", (), self.onMyPrivKey),
            #("GetContacts", (), self.onContacts),
            ("GetPubKey", (), self.onContactPubKey),
            ("GetContactPubKeys", (), self.onContactPubKeys),
            ("GetSeedNodes", (), self.onSeedNodes),
            #("Echo", ("TEST",), self.onEcho)
            #("RegisterListener", ("TESTLISTENER",), self.onRegisterListener)
            #("SendListener", ("TESTLISTENER",), self.onSendListener)
            ]
        if self.env.isIncoming:
            chain.append( ("Accept", (), self.onAccept) )
        elif self.env.isContactAction:
            chain.append( ("Connect", (), self.onConnect) )

        self.conn.chainCommands(chain, self.onError)
        
    
    def onOpen(self, result):
        print "Connection opened."
        
    def onMyPubKey(self, pubkey):
        print "My pub key: %i bytes" % len(pubkey)
    
    def onMyPrivKey(self, privkey):
        print "My priv key: %i bytes" % len(privkey)

    def onContactPubKey(self, pubkey):
        print "Contact pub key: %i bytes" % len(pubkey)
    
    def onSeedNodes(self, nodes):
        print "Seed Nodes:"
        for node in nodes:
            print "  %s:%i" % node
            
    def onContacts(self, contacts):
        print "Contact names:"
        for cname in contacts:
            print "  %s" % cname
            
    def onContactPubKeys(self, result):
        print "Contact list:"
        for cname in result:
            print "  %s: %s" % (cname, "%i byte key" % len(result[cname]))
        
    def onEcho(self, result):
        print "Echo: %s" % result
    
    def onAccept(self, sock):
        print "Accepted remote connection."
        
        # Set up the RPC callee
        self.rpcConn = RPCConnection( sock, self.reactor )
        # Set up the switchboard (?)
        self.switchboard = RPCSwitchboard( self.rpcConn )
        # Set up a FileServer instance, and serve files
        self.fileSystem = SimpleFS(os.path.expanduser("~/CSpaceShare"))
        # until the connection is closed.
        self.fileServer = FileServer(self.fileSystem, self.switchboard)
        self.rpcConn.setCloseCallback( self.onRPCClose )
    
    def onConnect(self, sock):
        print "Remote connection established."
        
        # Set up the rpc caller
        self.rpcConn = RPCConnection( sock, self.reactor )
        # Set up a FileClient instance
        self.fileClient = FileClient( self.rpcConn )
        self.rpcConn.setCloseCallback( self.onRPCClose )
        
        # Set up a xxxHTTPServer instance
        ShareRequestHandler.shareServer = self
        self.httpServer = SimpleHTTPServer(('127.0.0.1',0),
                                             self.reactor,
                                             ShareRequestHandler)
        self.httpServerPort = self.httpServer.server_port
        
        # Open the root webpage.
        webbrowser.open(self.getUrl("/"))
        
    def onRPCClose(self):
        #if self.env.isContactAction:
        #    self.conn.command("Connect", (), self.onConnect)
        #else:
        self.shutdown()
    
    def getUrl(self, path="/"):
        return "http://localhost:%i%s" % (self.httpServerPort, path)




def _quote_html(html):
    return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class ShareRequestHandler(HTTPRequestHandler):
    shareServer = None
    testResponse = "<HTML><BODY>Hello World.</BODY></HTML>"
    # For streaming
    BLOCKSIZE = 16384
    
    def do_GET(self):
        """Serve a GET request."""
        # Try to list the path
        self.path = self._translate_path()
        if self.path == "" or self.path[-1] != "/":
            self.path += "/"
        if self.path[0] != "/":
            self.path = "/" + self.path
        self.shareServer.fileClient.callList(self.path, self._GET_onList)
        self.state = self.WAITING
        self.content_type = ""
        return False

    # Directory listing    
    def _GET_onList(self, err, result):
        if err != 0:
            self.path = self.path[:-1]
            self.shareServer.fileClient.callGetSize(self.path, self._GET_onGetSize)
            return
        
        # Check for an index.html, index.htm
        if 'index.htm' in result:
            self.path += "index.htm"
            self.shareServer.fileClient.callGetSize(self.path, self._GET_onGetSize)
            return
        elif 'index.html' in result:
            self.path += "index.html"
            self.shareServer.fileClient.callGetSize(self.path, self._GET_onGetSize)
            return
        
        
        response = ""
        displaypath = cgi.escape(urllib.unquote(self.path))
        response += ("<title>Directory listing for %s</title>\n" % displaypath)
        response += ("<h2>Directory listing for %s</h2>\n" % displaypath)
        response += ("<hr>\n<ul>\n")
        if self.path != "/":
            parentDir = posixpath.dirname(self.path[:-1])
            response += ('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(parentDir), cgi.escape("..")))
            
        result.sort(key=lambda a: a.lower())
        for name in result:
            fullname = os.path.join(self.path, name)
            displayname = linkname = name
            response += ('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        response += ("</ul>\n<hr>\n")        
        
        self.content_type = "text/html"
        self.response_body = response
        self.response_bodylen = len(response)
        self._send_headers()
        self.stream.writeData(response)
        self.finishRequest()
    
    def _GET_onGetSize(self, err, result):
        if err != 0:
            self.send_error(404)
            self.finishRequest()
            return

        self.response_bodylen = result
        self._send_headers()

        self.fetch_start = 0
        fetchSize = self.BLOCKSIZE
        if result < fetchSize:
            fetchSize = result
        self.shareServer.fileClient.callRead(self.path, self.fetch_start, fetchSize, self._fetchMore)
            
    def _fetchMore(self, err, result):
        if err != 0:
            self.send_error(500)
            return

        self.stream.writeData(result)
        if self.fetch_start + len(result) == self.response_bodylen:
            self.finishRequest()
        else:
            self.fetch_start += self.BLOCKSIZE
            fetchSize = self.BLOCKSIZE
            if self.response_bodylen - self.fetch_start < fetchSize:
                fetchSize = self.response_bodylen - self.fetch_start
            self.shareServer.fileClient.callRead(self.path, self.fetch_start, fetchSize, self._fetchMore)
    
    def _send_headers(self):
        self.send_response(200)
        if not self.content_type:
            self.content_type = self.guess_type(self.path)
        self.send_header("Content-type", self.content_type)
        self.send_header("Content-Length", str(self.response_bodylen))
        self.end_headers()


    def do_HEAD(self):
        """Serve a HEAD request."""
        #f = self.send_head()
        #if f:
        #    f.close()
        self._resp_HEAD()
        return False
        
    def _resp_HEAD(self):
        self._send_headers()
    
    def do_POST(self):
        """Serve a POST request."""
        self.body_readlen = int(self.headers["content-length"])
        return True
    
    def do_POST_body(self):
        self._resp_POST()
        
    def _resp_POST(self):
        self._send_headers()
        self.stream.writeData(self.testResponse)


    def _translate_path(self):
        path = urlparse.urlparse(self.path)[2]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = ""
        nWord = -1
        for word in words:
            nWord += 1
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            if word == "" and nWord != 0 and nWord != len(words) - 1: continue
            path = os.path.join(path, word)
        return path

    def guess_type(self, path):
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']
    
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/x-python',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })

    
if __name__ == "__main__":
    if not os.getenv('CSPACE_PORT'):
        setEnviron()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    #initializeLogFile("ShareServer.log")
    ShareService().run()

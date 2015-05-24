import StringIO
import cspace.ext.storefwd
import urlparse, os.path, posixpath, urllib, cgi
import time, socket
import BaseHTTPServer, mimetools
import sys, logging
from nitro.tcp import TCPStream
import xmlrpclib
from xmlrpclib import Fault

logger = logging.getLogger()

DEFAULT_ERROR_MESSAGE = """\
<head>
<title>Error response</title>
</head>
<body>
<h1>Error response</h1>
<p>Error code %(code)d.
<p>Message: %(message)s.
<p>Error code explanation: %(code)s = %(explain)s.
</body>
"""


def _quote_html(html):
    return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SimpleHTTPServer:
    """ A slight re[f]actoring of SimpleHTTPServer """
    request_queue_size = 5
    
    def __init__(self, address, reactor, RequestHandlerClass):
        self.RequestHandlerClass = RequestHandlerClass
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.socket.bind(address)
        host, port = self.socket.getsockname()[:2]
        self.server_name = host #socket.getfqdn(host)
        self.server_port = port
        self.socket.listen(self.request_queue_size)
        self.activeRequests = []
        self.reactor = reactor
        self.reactor.addReadCallback(self.socket, self.onIncomingConnection)
        self.reactor.addExceptionCallback(self.socket, self.close)
        
    def close(self):
        self.socket.close()
    
    def onIncomingConnection(self):
        reqSocket, clientAddress = self.socket.accept()        
        request = self.RequestHandlerClass(reqSocket, clientAddress, self, self.reactor)
        self.activeRequests.append(request)
        
    def onRequestFinished(self, request):
        self.activeRequests.remove(request)



class HTTPRequestHandler:
    rbufsize = -1
    wbufsize = 0
    sys_version = "Python/" + sys.version.split()[0]
    server_version = "ReactionHTTP/0.1"
    protocol_version = "HTTP/1.1"
    
    (HANDLE_REQUESTS,
     READ_REQUEST_LINE,
     READ_HEADERS,
     READ_BODY,
     HANDLE_REQUEST,
     WAITING,
     FINISHING,
     CLOSING) = range(8)
    
    def __init__(self, connection, clientAddress, server, reactor):
        self.connection = connection
        self.clientAddress = clientAddress
        self.server = server
        self.reactor = reactor
        #self.wfile = self.connection.makefile('wb', self.wbufsize)
        self.stream = TCPStream(self.connection, self.reactor)
        self.stream.setInputCallback(self._onInput)
        self.stream.setErrorCallback(self._onError)
        self.state = self.HANDLE_REQUESTS
        self.stream.initiateRead( 1 )

    def _onError(self, result, notify):
        self.close()
        self.server.onRequestFinished(self)
    
    def _onInput(self, data):
        if self.state == self.HANDLE_REQUESTS:
            self.close_connection = 1
            self.raw_requestline = ""
            self.raw_headers = ""
            self.body = ""
            self.state = self.READ_REQUEST_LINE
            
        if self.state == self.READ_REQUEST_LINE:
            self.raw_requestline += data
            if self.raw_requestline.endswith("\r\n"):
                result = self.parse_requestline()
                if not result:
                    self.state = self.CLOSING
                else:
                    self.raw_headers = ""
                    self.state = self.READ_HEADERS

        elif self.state == self.READ_HEADERS:
            self.raw_headers += data
            if self.raw_headers.endswith("\r\n\r\n"):
                self.parse_headers()
                self.state = self.HANDLE_REQUEST

        elif self.state == self.READ_BODY:
            self.body += data
            # TODO: Determine when we're done.
            if len(self.body) == self.body_readlen:
                self.handle_requestbody()
                self.body = ""
        
        if self.state == self.HANDLE_REQUEST:
            read_body = self.handle_request()
            if not self.state == self.WAITING:
                if self.close_connection:
                    self.state = self.CLOSING
                elif read_body:
                    self.state = self.READ_BODY
                else:
                    self.state = self.READ_REQUEST_LINE
                self.raw_requestline = ""
                self.raw_headers = ""
                self.body = ""
                
        if self.state in (self.CLOSING, self.FINISHING):
            self.finishRequest()
    
    def finishRequest(self):
        if self.state == self.CLOSING or self.close_connection == 1:
            self.close()
            self.server.onRequestFinished(self)

    def parse_requestline(self):
        self.command = None  # set in case of error on the first line
        self.request_version = version = "HTTP/0.9" # Default
        self.close_connection = 1
        requestline = self.raw_requestline
        if requestline[-2:] == '\r\n':
            requestline = requestline[:-2]
        elif requestline[-1:] == '\n':
            requestline = requestline[:-1]
        self.requestline = requestline
        words = requestline.split()
        if len(words) == 3:
            [command, path, version] = words
            if version[:5] != 'HTTP/':
                self.send_error(400, "Bad request version (%r)" % version)
                return False
            try:
                base_version_number = version.split('/', 1)[1]
                version_number = base_version_number.split(".")
                # RFC 2145 section 3.1 says there can be only one "." and
                #   - major and minor numbers MUST be treated as
                #      separate integers;
                #   - HTTP/2.4 is a lower version than HTTP/2.13, which in
                #      turn is lower than HTTP/12.3;
                #   - Leading zeros MUST be ignored by recipients.
                if len(version_number) != 2:
                    raise ValueError
                version_number = int(version_number[0]), int(version_number[1])
            except (ValueError, IndexError):
                self.send_error(400, "Bad request version (%r)" % version)
                return False
            if version_number >= (1, 1) and self.protocol_version >= "HTTP/1.1":
                self.close_connection = 0
            if version_number >= (2, 0):
                self.send_error(505,
                          "Invalid HTTP Version (%s)" % base_version_number)
                return False
        elif len(words) == 2:
            [command, path] = words
            self.close_connection = 1
            if command != 'GET':
                self.send_error(400,
                                "Bad HTTP/0.9 request type (%r)" % command)
                return False
        elif not words:
            return False
        else:
            self.send_error(400, "Bad request syntax (%r)" % requestline)
            return False
        
        self.command, self.path, self.request_version = command, path, version
        return True

    def parse_headers(self):
        headerFile = StringIO.StringIO(self.raw_headers)
        self.headers = self.MessageClass(headerFile, 0)

        conntype = self.headers.get('Connection', "")
        if conntype.lower() == 'close':
            self.close_connection = 1
        elif (conntype.lower() == 'keep-alive' and
              self.protocol_version >= "HTTP/1.1"):
            self.close_connection = 0
    
    def handle_request(self):
        mname = 'do_' + self.command
        if not hasattr(self, mname):
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        method = getattr(self, mname)
        return method()
    
    def handle_requestbody(self):
        mname = 'do_' + self.command + '_body'
        if not hasattr(self, mname):
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        method = getattr(self, mname)
        return method()
        
    error_message_format = DEFAULT_ERROR_MESSAGE

    def send_error(self, code, message=None):
        try:
            short, long = self.responses[code]
        except KeyError:
            short, long = '???', '???'
        if message is None:
            message = short
        explain = long
        self.log_error("code %d, message %s", code, message)
        # using _quote_html to prevent Cross Site Scripting attacks (see bug #1100201)
        content = (self.error_message_format %
                   {'code': code, 'message': _quote_html(message), 'explain': explain})
        self.send_response(code, message)
        self.send_header("Content-Type", "text/html")
        self.send_header('Connection', 'close')
        self.end_headers()
        if self.command != 'HEAD' and code >= 200 and code not in (204, 304):
            self.stream.writeData(content)


    def send_response(self, code, message=None):
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.stream.writeData("%s %d %s\r\n" %
                             (self.protocol_version, code, message))
            # print (self.protocol_version, code, message)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())

    def send_header(self, keyword, value):
        """Send a MIME header."""
        if self.request_version != 'HTTP/0.9':
            self.stream.writeData("%s: %s\r\n" % (keyword, value))

        if keyword.lower() == 'connection':
            if value.lower() == 'close':
                self.close_connection = 1
            elif value.lower() == 'keep-alive':
                self.close_connection = 0

    def end_headers(self):
        """Send the blank line ending the MIME headers."""
        if self.request_version != 'HTTP/0.9':
            self.stream.writeData("\r\n")

    def log_request(self, code='-', size='-'):
        self.log_message('"%s" %s %s',
                         self.requestline, str(code), str(size))

    def log_error(self, *args):
        self.log_message(*args)
        
    def log_message(self, format, *args):
        global logger
        logger.info("%s - - [%s] %s\n" %
                     (self.address_string(),
                      self.log_date_time_string(),
                      format%args))

    def version_string(self):
        """Return the server software version string."""
        return self.server_version + ' ' + self.sys_version

    def date_time_string(self):
        """Return the current date and time formatted for a message header."""
        now = time.time()
        year, month, day, hh, mm, ss, wd, y, z = time.gmtime(now)
        s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
                self.weekdayname[wd],
                day, self.monthname[month], year,
                hh, mm, ss)
        return s

    def log_date_time_string(self):
        """Return the current time formatted for logging."""
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        s = "%02d/%3s/%04d %02d:%02d:%02d" % (
                day, self.monthname[month], year, hh, mm, ss)
        return s
    
    monthname = BaseHTTPServer.BaseHTTPRequestHandler.monthname
    weekdayname = BaseHTTPServer.BaseHTTPRequestHandler.weekdayname
    MessageClass = mimetools.Message
    
    def address_string(self):
        host, port = self.clientAddress[:2]
        return socket.getfqdn(host)
    
    responses = BaseHTTPServer.BaseHTTPRequestHandler.responses

    def close(self):
        self.stream.close(deferred=True, callback=self.connection.close)
        
    

class XMLRPCRequestHandler(HTTPRequestHandler):
    """ Ripped off from SimpleXMLRPCServer.
        Modified to use the reactor pattern. """
    async = False
    
    def do_POST(self):
        # We want the body.
        self.body_readlen = int(self.headers["content-length"])
        return True
    
    def do_POST_body(self):
        self.state = self.WAITING
        self.worker = threading.Thread(target=self._marshaled_dispatch)

    def _onResponse(self):
        # got a valid XML RPC response
        self.send_response(200)
        self.send_header("Content-type", "text/xml")
        self.send_header("Content-length", str(len(self.response_body)))
        self.end_headers()
        self.stream.writeData(response)

        # shut down the connection
        self.close()
        self.server.finalizeRequest()
        
    def _marshaled_dispatch(self):
        try:
            params, method = xmlrpclib.loads(self.body)
            func = self._findMethod(method)
            response = func(*params)
            # wrap response in a singleton tuple
            response = (response,)
            response = xmlrpclib.dumps(response, methodresponse=1)
        except Fault, fault:
            response = xmlrpclib.dumps(fault)
        except:
            # report exception back to server
            response = xmlrpclib.dumps(
                xmlrpclib.Fault(1, "%s:%s" % (sys.exc_type, sys.exc_value))
                )
        self.response_body = response
        self._onResponse()

 
    def _findMethod(self, method):
        func = None
        try:
            # check to see if a matching function has been registered
            func = self.funcs[method]
        except KeyError:
            if self.instance is not None:
                # check for a _dispatch method
                if hasattr(self.instance, '_dispatch'):
                    return self.instance._dispatch(method, params)
                else:
                    # call instance method directly
                    try:
                        func = resolve_dotted_attribute(
                            self.instance,
                            method,
                            self.allow_dotted_names
                            )
                    except AttributeError:
                        pass

        if func is None:
            error = Exception('method "%s" is not supported' % method)
            if not self.async:
                raise error
            else:
                self._asyncResponse(None, error)
        return func




class XMLRPCAsyncRequestHandler(XMLRPCRequestHandler):
    async = True
    
    def do_POST_body(self):
        self._marshaled_dispatch()

    def _marshaled_dispatch(self):
        params, method = xmlrpclib.loads(self.body)
        func = self._findMethod(method)
        if func is not None:
            args = tuple(params) + (self.server.reactor, self._asyncResponse)
            func(*args)

    def _asyncResponse(self, response=None, fault=None):
        if response:
            try:
                response = (response,)
                response = xmlrpclib.dumps(response, methodresponse=1)
            except Fault, fault:
                response = xmlrpclib.dumps(fault)
        elif fault:
            if type(fault) is Fault:
                response = xmlrpclib.dumps(fault)
            else:
                # report exception back to server
                response = xmlrpclib.dumps(
                    xmlrpclib.Fault(1, "%s:%s" % (type(fault), fault))
                    )

        self._onResponse(response)



class XMLRPCServer(SimpleHTTPServer):
    def __init__(self, address, reactor, RequestHandler):
        SimpleHTTPServer.__init__(self, address, reactor, RequestHandler)
        self.funcs = {}
        self.instance = None

    def register_instance(self, instance, allow_dotted_names=False):
        self.instance = instance
        self.allow_dotted_names = allow_dotted_names

    def register_function(self, function, name = None):
        if name is None:
            name = function.__name__
        self.funcs[name] = function



#!/usr/bin/python
# CSpaceControl - Main CSpace service controller
# (C) 2007 Tachyon, CptnAhab
# Each command line argument is a command (with a few options betwixt)
# Available commands:
#   'update' check for and download any CSpace updates
#   'about'  display some basic CSpace info
#   'startnet <options>' to launch CSpace DHT/Router node daemon
#   'statusnet' to check CSpace DHT/Router node status
#   'stopnet' to kill CSpace DHT/Router node daemon
#   'init' to generate crypto identity and register with key server
#   'initlocal' to generate crypto identity, but not register with server
#   'switch <profile> <password>' to change profiles
#   'start <options>' to launch CSpace daemon
#   'restart <options>' to kill and restart CSpace daemon
#   'online' to put the daemon online
#   'svcstatus' to check CSpace connection status
#   'offline' to take the daemon offline
#   'list' to list buddies and their status/services
#   'add <buddy> <keyid>' to add a buddy to your list
#   'remove <buddy>' to remove a buddy from your list
#   'connect <buddy> <service>' to connect to a buddy+service
#   'buddy <buddy>' to retrieve buddy info
#   'probe <buddy>' to recheck buddy status now

import os, os.path, sys, logging
import time, xmlrpclib, urllib

# Import some constants, and a utility function
from cspace.main.autoupdater import UPDATE_BASE_URL, UPDATE_LATEST_VERSION, currentBuildNumber
from cspace.main.service import getPIDpath
from cspace.main.common import isValidUserName, localSettings
from cspace.main.profile import createProfile, listProfiles, loadProfile
from ncrypt.rsa import RSAKey, RSAError
from ncrypt.digest import DigestType, Digest
from nitro.async import AsyncOp
from nitro.http import HttpRequest
from nitro.selectreactor import SelectReactor
from cspace.util.hexcode import hexDecode


def _getOurLocation() :
    fpath = os.path.abspath(os.path.realpath(__file__))
    pwd = os.path.dirname( fpath )
    return pwd

def _setupPythonPath() :
    # Make sure that we include the CSpace code library
    pwd = _getOurLocation()
    sys.path.append( pwd )
    # sys.path doesn't propagate to subprocesses (applets)
    if os.environ.has_key( 'PYTHONPATH' ) :
        if pwd in os.environ['PYTHONPATH'] :
            return
        if sys.platform == 'win32' :
            s = ';%s' % pwd
        else :
            s = ':%s' % pwd
        os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + s
    else :
        os.environ['PYTHONPATH'] = pwd





class CSpaceServiceController:
    def __init__(self):
        self._netserver = None
        self._server = None
        self.buildNumber = currentBuildNumber()

    def _getserviceinfo(self):
        pidpath = getPIDpath()
        if not os.path.exists(pidpath) or not os.path.isfile(pidpath):
            return None, None, None
        fInfo = open(pidpath)
        pid = int(fInfo.readline())
        port = int(fInfo.readline())
        applet = int(fInfo.readline())
        return pid, port, applet

    def _getnetserviceinfo(self):
        pidpath = getPIDpath("CSpaceNetwork")
        if not os.path.exists(pidpath) or not os.path.isfile(pidpath):
            return None, None
        fInfo = open(pidpath)
        pid = int(fInfo.readline())
        port = int(fInfo.readline())
        return pid, port

    def _getserver(self, netserver=False):
        if self._server is None:
            pid, port, applet = self._getserviceinfo()
            if pid is None:
                return None
            self._server = xmlrpclib.Server("http://localhost:%i/" % port)
        return self._server

    def _getnetserver(self):
        if self._netserver is None:
            pid, port = self._getnetserviceinfo()
            if pid is None:
                return None
            self._netserver = xmlrpclib.Server("http://localhost:%i/" % port)
        return self._netserver

    def about(self):
        server = self._getserviceinfo()
        server2 = self._getnetserviceinfo()

        print "-----------------------------------"
        print "    About CSpace, CSpaceControl    "
        print "  CSpaceService and CSpaceNetwork  "
        print "Peer-to-Peer Communication Platform"
        if server[0] != None:
            print "-----------------------------------"
            print "         CSpaceService         "
            print "     XMLRPC Server Port: %i" % server[1]
            print "     Applet Server Port: %i" % server[2]
        if server2[0] != None:
            print "-----------------------------------"
            print "           CSpaceNetwork           "
            print "     XMLRPC Server Port: %i" % server2[1]
        print "-----------------------------------"
        print "            Build # %i " % self.buildNumber
        print "     (C) Tachyon Technologies      "
        print "             2006-2007             "
        print "-----------------------------------"

    def update(self):
        """ Returns True if an update was downloaded
            and installed. """
        print "Checking for CSpace updates..."

        # Load the list of installers
        try:
            fLatest = urllib.urlopen(UPDATE_BASE_URL + UPDATE_LATEST_VERSION)
            files = fLatest.read().split("\r\n")
            fLatest.close()
        except:
            print "Could not retrieve %s: %s" % (UPDATE_LATEST_VERSION,
                                                 sys.exc_info()[0])
            return False

        # Sort the list by decreasing build number
        outfiles = []
        for f in files:
            if f == "":
                continue
            fileName,fileSize,buildNumber,requires = f.strip().split(":")
            outfiles.append( (-int(buildNumber),int(fileSize),int(requires),fileName, int(buildNumber)) )
        files = outfiles
        files.sort()

        print "Found %i possible updates." % len(files)

        print "Checking for most appropriate update from %i..." % self.buildNumber
        for f in range(len(files)):
            sb,fileSize,requires,fileName,buildNumber = files[f]

            # If we're already up-to-date, skip the rest.
            if buildNumber <= self.buildNumber:
                print "Already up-to-date!"
                return False

            # If we're not sufficiently up-to-date,
            # don't download this installer
            if requires > self.buildNumber:
                continue

            # Download it and install it!
            url = UPDATE_BASE_URL + fileName
            try:
                fn, hdrs = urllib.urlretrieve(url, fileName)
            except IOError:
                print "Could not retrieve %s: %s" % (fileName,
                                                     sys.exc_info()[0])
                return False

            print "Successfully downloaded %s." % fn
            return True

        print "No appropriate updates found."
        return False


    def _generateKey(self, username):
        if not isValidUserName(username):
            print "Invalid username: %s" % username
            print ('Only lowercase alphabets(a-z), ' +
                    'digits(0-9), and underscore(\'_\') are allowed ' +
                    'in the username.')
            return

        print "Creating public key..."
        rsaKey = RSAKey()
        rsaKey.generate( bits=2048 )
        return rsaKey

    def _saveProfile(self, username, password, rsaKey):
        print "Saving settings..."
        st = localSettings()
        st.setString('Settings/SavedProfile', username)
        st.setString('Settings/SavedPassword', password)
        st.setInt('Settings/RememberKey', 1)

        print "Saving profile..."
        createProfile(rsaKey, password, username, str(self._keyId))
        del self._keyId
        del self._reactor
        print "New identity %s created." % username

    def localinit(self, username, password):
        print "Generating new CSpace identity..."
        rsaKey = self._generateKey(username)
        self._keyId = -1
        self._reactor = None
        self._saveProfile(username, password, rsaKey)

    def init(self, username, password):
        print "Generating new CSpace identity..."
        rsaKey = self._generateKey(username)

        data = 'username:%s' % username
        digestType = DigestType( 'SHA1' )
        digest = Digest(digestType).digest( data )
        signature = rsaKey.sign( digest, digestType )

        form = dict( username=username,
                public_key=rsaKey.toDER_PublicKey(),
                signature=signature )
        postData = urllib.urlencode( form )

        self._reactor = SelectReactor()
        request = HttpRequest( self._reactor )
        httpOp = request.post( 'http://cspace.in/addkey', postData,
                               self._onRegisterResponse )
        self._keyId = -1
        print "Registering your public key..."
        self._reactor.run()
        if self._keyId < 0 :
            print "Failed to register your public key."
            return

        self._saveProfile(username, password, rsaKey)

    def _onRegisterResponse( self, returnCode, data ) :
        if returnCode != 200 :
            self._keyId = -1
        else:
            try :
                keyId = int(data)
                self._keyId = keyId
            except ValueError :
                self._keyId = -1
        self._reactor.stop()

    def switch(self, username, password):
        server = self._getserver()
        if server is not None:
            status = server.svcstatus()
            if status not in ("Offline", "Connect failed.",
                              "Disconnected"):
                print "Service is not Offline."
                return

        print "Switching to CSpace profile %s..." % username
        for profile in listProfiles():
            if profile[0] == username:
                break
            else:
                profile = None

        if profile is not None:
            profile = loadProfile(username, password)
            if profile is None:
                print "Incorrect password for profile."
                return
        else:
            print "No profile %s found." % username
            return

        print "Saving settings..."
        st = localSettings()
        st.setString('Settings/SavedProfile', username)
        st.setString('Settings/SavedPassword', password)
        st.setInt('Settings/RememberKey', 1)

    def startnet(self, args):
        print "Starting CSpace Network service..."
        installpath = _getOurLocation()
        args = [ 'python', os.path.join(installpath, 'CSpaceNetwork.py') ] + args
        try:
            pid = os.spawnve(os.P_NOWAIT, sys.executable, args, os.environ)
            print "Successfully started CSpace Network service - PID %i" % pid
        except:
            print "Failed to start CSpace Network service: %s" % sys.exc_info()[0]

    def statusnet(self):
        print "# Checking CSpace service status..."
        pid, port = self._getnetserviceinfo()
        if pid is not None:
            print "# CSpace Network service is started."
            print "PID=%i" % pid
            print "XMLRPC=%i" % port
        else:
            print "# CSpace Network service is not started."

    def stopnet(self):
        print "Stopping CSpace Network service..."
        server = self._getnetserver()
        if server is None:
            print "Network Service not started."
        else:
            server.stop()

    def start(self, args):
        print "Starting CSpace service..."
        installpath = _getOurLocation()
        args = [ 'python', '"' + os.path.join(installpath, 'CSpaceService.py') + '"' ] + args
        try:
            pid = os.spawnve(os.P_NOWAIT, sys.executable, args, os.environ)
            print "Successfully started CSpace service - PID %i" % pid
        except:
            print "Failed to start CSpace service: %s" % sys.exc_info()[0]

    def stop(self):
        print "Stopping CSpace service..."
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            server.stop()



    def status(self):
        print "# Checking CSpace service status..."
        pid, port, applet = self._getserviceinfo()
        if pid is not None:
            print "# CSpace service is started."
            print "PID=%i" % pid
            print "XMLRPC=%i" % port
            print "APPLET=%i" % applet
        else:
            print "# CSpace service is not started."


    def restart(self, args):
        print "Re-starting CSpace service..."
        server = self._getserver()
        if server is not None:
            self.stop()
            time.sleep(10)
        else:
            print "Server was not running."
        self.start(args)


    def online(self):
        print "Logging into CSpace..."
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            result = server.online()
            print "Response: %s" % str(result)

    def svcstatus(self):
        print "Checking CSpace connection status..."
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            result = server.svcstatus()
            print "Response: %s" % str(result)

    def offline(self):
        print "Logging out of CSpace..."
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            result = server.offline()
            print "Response: %s" % str(result)

    def add(self, buddy, keyid):
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            result = server.add(buddy, keyid)
            print "Response: %s" % str(result)

    def remove(self, buddy):
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            result = server.remove(buddy)
            print "Response: %s" % str(result)

    def list(self):
        print "Listing CSpace buddies..."
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            buddies = server.list()
            if buddies[0] is False:
                print "Not connected."
                return
            for buddystatus in buddies:
                print "%s: (%i) %s" % tuple(buddystatus)

    def probe(self, buddy):
        print "Probing CSpace buddy %s..." % buddy
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            result = server.probe(buddy)
            print "Result: %s" % result

    def buddy(self, buddy):
        print "Retrieving CSpace buddy %s info..." % buddy
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            result = server.contactinfo(buddy)
            if result[0] == False:
                print "Error: %s" % str(result[1:])
            else:
                print "Name: %s" % str(result[0])
                print "PublicKey: %s" % str(result[1])
                print "Status: %s" % str(result[2])

    def action(self, buddy, action):
        """ Create a localip:port tunnel to remoteip:rport, and
        run a child process there and here. """
        print "Connecting to CSpace buddy %s, action %s..." % (buddy, action)
        server = self._getserver()
        if server is None:
            print "Service not started."
        else:
            result = server.action(buddy, action)
            print "Response: %s" % str(result)


def main():
    service = CSpaceServiceController()

    commands = {
        "about": (service.about, 0),
        "update": (service.update, 0),
        "init": (service.init, 2),
        "localinit": (service.localinit, 2),
        "start": (service.start, 0),
        "switch": (service.switch, 2),
        "restart": (service.restart, 0),
        "status": (service.status, 0),
        "stop": (service.stop, 0),
        "startnet": (service.startnet, 0),
        "statusnet": (service.statusnet, 0),
        "stopnet": (service.stopnet, 0),
        "online": (service.online, 0),
        "svcstatus": (service.svcstatus, 0),
        "offline": (service.offline, 0),
        "list": (service.list, 0),
        "action": (service.action, 2),
        "add": (service.add, 2),
        "remove": (service.remove, 1),
        "probe": (service.probe, 1),
        "buddy": (service.buddy, 1),
    }

    args = sys.argv[1:]
    while len(args):
        command = args.pop(0).lower()
        if command in commands:
            func, argcount = commands[command]
            funcargs = args[0:argcount]
            if command == "update":
                if func(*funcargs):
                    args.append("restart")
            elif command in ("start", "restart", "startnet"):
                # Start and restart pass options
                # ie. everything up to the next command
                # or end of the command line
                while len(args) and args[0] not in commands:
                    funcargs.append(args.pop(0))
                func(funcargs)
            else:
                func(*funcargs)

            args = args[argcount:]
        else:
            print "Unknown command '%s'" % command

if __name__ == '__main__' :
    if not hasattr(sys,'frozen') :
        _setupPythonPath()
    main()

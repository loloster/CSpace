#!/usr/bin/python

from cspace.main.service import CSpaceService
import sys, logging, time
import cspace.ext.storefwd

class TestApplication:
    def __init__(self, local=False):
        if local:
            seedNodes = [('127.0.0.1', 10001)]
        else:
            seedNodes = [('210.210.1.102', 10001)]
        
        self.service = CSpaceService(seedNodes)
        self.reactor = self.service.reactor
        self.dispatcher = self.service.dispatcher
        
        self.dispatcher.register('service.start', self.onStarted)
        self.dispatcher.register('service.stop', self.onStopped)
        self.dispatcher.register('profile.connecting', self.onConnecting)
        self.dispatcher.register('profile.disconnecting', self.onDisconnecting)
        self.dispatcher.register('profile.online', self.onOnline)
        self.dispatcher.register('profile.offline', self.onOffline)
        self.dispatcher.register('contact.online', self.onUserOnline)
        self.dispatcher.register('contact.action', self.onUserAction)
        self.dispatcher.register('contacts.probing', self.onContactsProbing)
        self.dispatcher.register('contacts.probed', self.onContactsProbed)
        self.dispatcher.register('contact.offline', self.onUserOffline)
        self.dispatcher.register('offlineim.get', self.onOfflineReceive)
        self.dispatcher.register('offlineim.put', self.onOfflineStore)
        self.dispatcher.register('offlineim.del', self.onOfflineDelete)

    def onStarted(self):
        print "Started."
        self.service.online()
        
    def onConnecting(self, profile):
        print "Connecting..."

    def onOnline(self, profile):
        print "Online!"
    
    def onDisconnecting(self, profile):
        print "Disconnecting..."

    def onOffline(self, profile):
        print "Offline!"
        
    def onContactsProbing(self, contacts):
        print "Probing contact list..."
        print "  " + "\n  ".join(contacts)
    
    def onContactsProbed(self, contacts):
        print "Contacts probed."
        # Automatically goes offline first.
        self.reactor.callLater(15, self.service.stop)
        print "Waiting..."
        
    def onUserOnline(self, contact):
        print "User %s is online." % contact.name
        
    def onUserAction(self, contact, action, retval):
        if retval:
            print "Succesfully executed action %s on buddy %s." % (action, contact.name)
        else:
            print "Failed to execute action %s on buddy %s." % (action, contact.name)
    
    def onUserOffline(self, contact):
        print "User %s is offline." % contact.name
        
    def onOfflineReceive(self, ts, msg, peerPubKey):
        print "Received offline message."
        
    def onOfflineStore(self, msg):
        print "Stored offline message."
        
    def onOfflineDelete(self, envelope):
        print "Deleted offling message."

    def onStopped(self):
        print "Stopped!"
    
    def run(self):
        # Just to get the ball rolling.
        self.service.run()
        print "All done!"
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)30s    %(levelname)5s   %(message)s',
                        filename='/tmp/cspacetest.log',
                        filemode='w')
    app = TestApplication(True)
    print "Starting..."
    app.run()
    time.sleep(1)

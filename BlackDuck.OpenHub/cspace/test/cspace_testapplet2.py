#!/usr/bin/env python
# CSpace ApplicationConnection Test

from cspaceapps.appletutil import ApplicationConnection, CSpaceEnv
from nitro.selectreactor import SelectReactor
from cspace.main.service import getPIDpath
import os, logging
import cspace.ext.storefwd

class TestApplet:
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
            chain.append( ("Connect", (None, "test"), self.onConnect) )

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
        self.shutdown()
    
    def onConnect(self, sock):
        print "Remote connection established."
        self.shutdown()
    
    def onRegisterListener(self, result):
        print "Listener registered."
    
    def onSendListener(self, result):
        print "Listener sent."
    
    
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

TestApplet().run()

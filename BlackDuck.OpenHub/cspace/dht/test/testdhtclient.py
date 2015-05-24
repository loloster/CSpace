import sys, os, logging
from socket import socket, AF_INET, SOCK_DGRAM
from nitro.selectreactor import SelectReactor
from ncrypt.rsa import RSAKey
from ncrypt.digest import Digest, DigestType
from cspace.util.hexcode import hexDecode
from nitro.bencode import encode as bencode
import cspace.ext.storefwd
import time

from cspace.dht import rpc
_requestCount = 0
_oldRequestMethod = rpc.RPCSocket.request
def _newRequestMethod( *args, **kwargs ) :
    global _requestCount
    _requestCount += 1
    return _oldRequestMethod( *args, **kwargs )
rpc.RPCSocket.request = _newRequestMethod

from cspace.dht.util import checkPort, toId
from cspace.dht.util import computeSignature
from cspace.dht.rpc import RPCSocket
from cspace.dht.client import DHTClient

logging.getLogger().addHandler( logging.StreamHandler() )

def NodeAddr( port ) :
    return ('127.0.0.1',port)

class TestClient( object ) :
    def __init__( self, nodeAddr ) :
        self.nodeAddr = nodeAddr
        self.sock = socket( AF_INET, SOCK_DGRAM )
        self.sock.bind( ('127.0.0.1',0) )
        print "Listening on %s:%i" % self.sock.getsockname()
        self.reactor = SelectReactor()
        self.rpcSocket = RPCSocket( self.sock, self.reactor )
        self.client = DHTClient( self.rpcSocket )
        self.client.timeout = 1.5
        self.client.retries = 1
        self.client.backoff = 1

    def _initCount( self ) :
        self.startRequestCount = _requestCount

    def _getCount( self ) :
        return _requestCount - self.startRequestCount

    def _doneCount( self ) :
        count = self._getCount()
        print 'request count =', count

    def _onResult( self, err, payload ) :
        print 'err=%d, payload=%s' % (err,str(payload))
        self._doneCount()
        self.reactor.stop()

    def Ping( self ) :
        self._initCount()
        self.client.callPing( self.nodeAddr, self._onResult )
        self.reactor.run()

    def GetAddr( self ) :
        self._initCount()
        self.client.callGetAddr( self.nodeAddr, self._onResult )
        self.reactor.run()

    def GetKey( self, publicKey ) :
        self._initCount()
        self.client.callGetKey( publicKey.toDER_PublicKey(),
                self.nodeAddr, self._onResult )
        self.reactor.run()

    def PutKey( self, rsaKey, data, updateLevel ) :
        self._initCount()
        signature = computeSignature( rsaKey, data, updateLevel )
        self.client.callPutKey( rsaKey.toDER_PublicKey(), data,
                updateLevel, signature, self.nodeAddr,
                self._onResult )
        self.reactor.run()
        
    def PutOffIM(self, publicKey, envelope ):
        self._initCount()
        self.client.callPutOffIM( publicKey.toDER_PublicKey(), envelope,
                self.nodeAddr, self._onResult )
        self.reactor.run()
        
    def GetOffIM(self, publicKey ):
        self._initCount()
        self.client.callGetOffIM( publicKey.toDER_PublicKey(),
                self.nodeAddr, self._onResult )
        self.reactor.run()
        

    def FindNodes( self, destId ) :
        self._initCount()
        self.client.callFindNodes( destId, self.nodeAddr, self._onResult )
        self.reactor.run()

    def Lookup( self, destId ) :
        def onResult( result ) :
            print 'result = %s' % str(result)
            self._doneCount()
            self.reactor.stop()
        self._initCount()
        self.client.lookup( destId, [self.nodeAddr], onResult )
        self.reactor.run()

    def LookupGetKey( self, publicKey ) :
        def onResult( result ) :
            print 'result = %s' % str(result)
            self._doneCount()
            self.reactor.stop()
        self._initCount()
        self.client.lookupGetKey( publicKey, [self.nodeAddr], onResult )
        self.reactor.run()
        
        
    def LookupGetOffIM( self, publicKey ):
        results = []
        def onResult( result ) :
            i = 0
            for msg in result:
                print "message %i: %i bytes" % (i, len(msg))
                i += 1
                results.append(msg)
            #print 'result = %s' % str(result)
            self._doneCount()
            self.reactor.stop()
        self._initCount()
        self.client.lookupGetOffIM( publicKey, [self.nodeAddr], onResult )
        self.reactor.run()
        return results

    def LookupPutKey( self, rsaKey, data, updateLevel ) :
        def onResult( successCount, latestUpdateLevel ) :
            print 'successCount=%d, latestUpdateLevel=%d' % (
                    successCount, latestUpdateLevel)
            self._doneCount()
            self.reactor.stop()
        self._initCount()
        self.client.lookupPutKey( rsaKey, data, updateLevel,
                [self.nodeAddr], onResult )
        self.reactor.run()

        
    def LookupPutOffIM( self, publicKey, envelope ):
        def onResult( result ) :
            print 'result = %s' % str(result)
            self._doneCount()
            self.reactor.stop()
        self._initCount()
        self.client.lookupPutOffIM( publicKey, envelope, [self.nodeAddr], onResult )
        self.reactor.run()
        
        
    def LookupDelOffIM( self, publicKey, envelope, signature ):
        def onResult( result ) :
            print 'result = %s' % str(result)
            self._doneCount()
            self.reactor.stop()
        self._initCount()
        self.client.lookupPutOffIM( publicKey, envelope, [self.nodeAddr], onResult )
        self.reactor.run()

def main() :
    pubdata = ("308201080282010100c3b196c56ad320fa97c390b3f79c8f643151a986236b" +
               "354b764adc90c9df2cf6ee713ba557a81495af4e7f683fdb77c55fe78e8211" +
               "ccab5b208a3c796f30e19b66f0466fe26e5dad9017cce9215eaa71f67dc978" +
               "596d656a4f64cab51951be3fb7a0eb77b65968e4325bd1604e53c761f533c5" +
               "264f36e2b3201084e57c7762d5fb573568df60de6f1a81761f9e18b59b7cb8" +
               "915924971d74e0b71029d433ca06b1ebb2290b8e00111c7a435d4b6f28b256" +
               "8e21201dbb8f45ab1e1e73eeba955b70a35c6c2fb3c196f5e46c3db061fbe6"+
               "54cda85a4ddedf3f1b2eec1c5cf8232b9d63d07140136b3be48edcd29024e7"+
               "73da992bf88117f97a4e72bfcfdfdd0583020105")
    
    privdata = """-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,ADAC35AAE233FCD7

V7O3FSD4U2+mqI67ZQ2ipijKS5/wQiPrrUCemKFnY57c3g8YeFwmy6U8ObOUJnl/
pM6DuTVxcm0bDd1kAIAlDve8Rj7VmIsfX0/d+EjWpM4DslwtItpHsIkMrcjRdn7i
gQtjyAOUmBY4GMG2tQY5WEJLyjfmoXw9Mm/8QGqI93OE+m71xjHPYdUvU98CSYUF
YiwpiJjzn3kU2owk4P7pkcdqKY04u+DGf3Oxg0UVwjOevK2EUyXAKDjJM5kpahU3
l9A49wAc83WeLy9aJE/Ci/P7b7nr/1eq2C9LlAosKZS4dyw7b1su+JfcEAvxp8mi
AIfXzjSkVCDSHcGyOvAjiNiJXAU2omuvaDZ15HLagXu2at0jBK60FhBi0w78+vbZ
WyPjXkG6DTKGCr/fUbIpefUcDtOCQI8DKVUllKV+6OIX/zEWjAMVgBUwNsHJA1Q+
Wmzfxv152RuGgBQ7Ne+bFd4PdLXwZlwF+Oct7AaTQrBOunRAQ6WJZT5vPqIfLD6y
A+MKEnJkU0aMmMKIzDnkPS1SENjjur+w818EI4wv0CF+DBGp1bji0VEfwVgQfAym
1HCpjcOnP+xY1OXPXOMBVixMEX3BJZR2WNeIpURm3w08wCsJckXoQ5ohvg6OkaKC
zdUZo8nGyMZJkaU2l4xhrgabqJ1yVeRK2FNZCoPINq/eoFWLOIiiPORaFxvMZIVe
9LSoAgJqbFRmKZnQT5YgBzOvrU44q1Z+g+S5aODX4MvfMNCKvAkSOBu0e01bV/18
YhNdsBVLHBKXeQ++kyfApS02AFj/UnTR7QMKxznUOUH7tDwdv57rvAXb6uLRv+jF
roc2EljDSz226oGR39NwpFsvQvDs8RUxJBCprb4jPCl5vV1eDqRAybhCa0Oahzsv
lGeoPvj7FghfNIdCdkcZTO0vz/EjLzH+R5IDG/InfzPLpV6nzZ8NFnUA6a5aleK2
1Y2d57XyAB82quQ2jXyzA6SFhBFg4rDvNmlVJBWgTWNHWyCbfotR4xPYUta4SbL+
RSPIu4tDMdY0SGtQ7vdlr8/ikpf4nssBSJFbUWZUMedy9yk7+eCcYS0GnXKnJfjO
tHnWSUBnuPum+z2XudNwyqjM9NrH1WAmUCGs71XAryRnoLjyNaoq2hcChWTxyxpt
N8CSQ5d07iy/hbZgA2puCXi0GQoz2IEBti4blb8KMn0IoiT1btFnPI7djds6Ci0c
ZKUl9mL5QjRWUMqBzREBkIyiEcTzhOWW6TjFV6/2WRCBLIsOCy0pV+TYLkZtP0Qi
LJBp+lPMhEw0Ae5cE16LYXma2IS4UoNtB2fyn5TPX8NHPSbWA54zGfTLHSSvzh0+
7LLm0fD14OS6CBbrjCnxCgFe7oRDg3wglGQVNr6gibS6gEMpRiZYkbB4jCyqoGH3
F8HVlAkLtcuzOWbXetXDkQZxP4KUWlxei7HlL48QIxBu6skCScs8vITJdUZc148N
uGF5Rms+gbVlSDxwzxwl7wQsydcxamKapH4wbF2CBhpZtI/Y+CrQIyOyXMA2UnBE
+agHes5L48ns26rJYA2lfIoKod2y2WsmdLTKmTV+KUpEAgU1XVF9vA==
-----END RSA PRIVATE KEY-----"""

    
    logging.getLogger().addHandler( logging.StreamHandler() )
    reactor = SelectReactor()
    seedNodeAddr1 = ('127.0.0.1',10001)
    seedNodeAddr2 = ('127.0.0.1',10001)
    print "Storing offline messages..."
    client1 = TestClient(seedNodeAddr1)
    pubKey = RSAKey()
    pubKey.fromDER_PublicKey( hexDecode( pubdata ) )
    #for n in range(3):
    #    client1.LookupPutOffIM(pubKey, 'Message #%i' % n)

    #time.sleep(3)

    print "Retrieving stored messages..."
    client2 = TestClient(seedNodeAddr2)    
    messages = client2.LookupGetOffIM(pubKey)

    #time.sleep(3)
    #
    #privKey = RSAKey()
    #privKey.fromPEM_PrivateKey( privdata, 'arrr' )
    #digestType = DigestType( "SHA1" )
    #for msg in messages:
    #    sigdata = bencode( ( pubdata, msg ) )
    #    digest = Digest( digestType ).digest( sigdata )
    #    signature = privKey.sign( digest, digestType )
    #    client1.LookupDelOffIM(pubKey, msg, signature)
    #    
if __name__ == "__main__":
    main()
    
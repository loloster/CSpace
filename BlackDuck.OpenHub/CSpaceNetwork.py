#!/usr/bin/python
import os, sys
import logging, socket
from SimpleXMLRPCServer import SimpleXMLRPCServer
import cspace.ext.storefwd

# The original commandline entry point
from cspace.network.node import startNetworkNode
from cspace.dht.node import DHTNode
from cspace.dht.rpc import RPCSocket
from cspace.dht.node import DHTNode

from nitro.selectreactor import SelectReactor
from cspace.main.app import LogFile
from cspace.main.common import localSettings
from cspace.main.service import getPIDpath


def startDHTNode( ipAddr, reactor, knownNodes, firstport ) :
    sock = None
    for portnum in range(firstport, firstport+9999):
        sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        nodeAddr = (ipAddr, portnum)
        try :
            sock.bind( nodeAddr )
        except socket.error :
            sock.close()
            sock = None
            continue
        else:
            break

    if sock is None: return None

    rpcSocket = RPCSocket( sock, reactor )
    node = DHTNode( rpcSocket, reactor, knownNodes )
    node.getAddr = lambda : nodeAddr
    return node


class NodeCluster:
    def __init__(self, options, reactor):
        self.reactor = reactor
        self.options = options
            
            
    def start(self):
        # Start nodes
        options = self.options
        logger = logging.getLogger()
        if options.dhtonly:
            nodeType = "DHT"
        else:
            nodeType = "Network"
        nodeFunc = globals()["start%sNode" % nodeType]
    
        # Client IP
        ipAddr = options.clientaddr
        self.nodes = []
        nodeList = []
        for n in range(options.nodecount):
            node = nodeFunc( ipAddr, self.reactor, options.knownnodes, options.firstport)
            if node is None :
                logger.error('unable to bind to any port on %s' % ipAddr)
                return
            nodeAddr = node.getAddr()
            msgArgs = tuple([nodeType] + list(nodeAddr))
            logger.info('started %s node address = %s:%i' % msgArgs)
            options.knownnodes.append( nodeAddr )
            nodeList.append(nodeAddr)
            options.firstport = nodeAddr[1]+1
            self.nodes.append(node)
        return nodeList

    def stop(self):
        for node in self.nodes:
            node.close()
        self.reactor.stop()
        return True



def _setupPythonPath() :
    # Make sure that we include the CSpace code library
    pwd = os.path.dirname( os.path.abspath(__file__) )
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

def _parseCommandLine():
    import optparse
    # Construct the command line argument handling
    oparser = optparse.OptionParser()

    oparser.add_option("-b", "--bind", dest="clientaddr",
                        help="bind to local IP", metavar="LOCALIP")
    oparser.add_option("-k", "--known", dest="knownnodes", action="append",
                        help="inject a known network node")
    oparser.add_option("-d", "--debug", dest="debug", action="store_true",
                        help="don't redirect stderr/stdout")
    oparser.add_option("-c", "--count", dest="nodecount", type="int",
                        help="start multiple network nodes on consecutive ports")
    oparser.add_option("-p", "--port", dest="firstport", type="int",
                        help="start first local node on port")
    oparser.add_option("-t", "--dht", dest="dhtonly", action="store_true",
                        help="start multiple network nodes on consecutive ports")
    oparser.add_option("-x", "--xmlrpc", dest="xmlport", type="int",
                        help="specify port for XMLRPC control")
    
    oparser.set_default('clientaddr', "127.0.0.1")
    oparser.set_default('debug', False)
    oparser.set_default("nodecount", 1)
    oparser.set_default("firstport", 10001)
    oparser.set_default("dhtonly", False)
    oparser.set_default("xmlport", 0)
    oparser.set_default("knownnodes", [])
    
    # Parse the command line
    (options, args) = oparser.parse_args()    
    return options, args


def _writePID(xmlrpcport):
    pidpath = getPIDpath("CSpaceNetwork")
    pidfile = file(pidpath, "wb")
    pidfile.write("%i\n%i\n" % (os.getpid(), xmlrpcport))
    pidfile.close()
    
def _deletePID():
    pidpath = getPIDpath("CSpaceNetwork")
    os.unlink(pidpath)    

def main() :
    # Command line
    options, args = _parseCommandLine()
    
    # Logging
    logger = logging.getLogger()
    settings = localSettings()
    if not options.debug:
        sys.stdout = sys.stderr = LogFile( settings, "CSpaceNetwork" )
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)        
    logging.getLogger('nitro.selectreactor').addHandler( logging.StreamHandler() )
    logger.addHandler( logging.StreamHandler() )
    
    # Host IPs        
    knownNodes = []
    prevIP = options.clientaddr
    for nodeAddr in options.knownnodes:
        try :
            ip,port = nodeAddr.split( ':' )
            if ip == "":
                ip = prevIP
            else:
                prevIP = ip
            port = int(port)
        except TypeError, ValueError :
            logger.error('invalid known node address: %s' % nodeAddr)
            return
        logger.info('known node address = %s:%i' % (ip,port))
        knownNodes.append( (ip,port) )
    options.knownnodes = knownNodes

    # Main loop
    reactor = SelectReactor()
        
    # Inter-process control
    server = SimpleXMLRPCServer(('localhost', options.xmlport))
    reactor.addReadCallback(server, server.handle_request)
    cluster = NodeCluster(options, reactor)
    server.register_instance(cluster, allow_dotted_names = True)
    options.xmlport = server.socket.getsockname()[1]
    logger.info("rpcserver listenport = %i" % options.xmlport)

    # Create all the nodes
    cluster.start()

    # And we're off!
    _writePID(options.xmlport)
    reactor.run()        
    _deletePID()


if __name__ == '__main__' :
    if not hasattr(sys,'frozen') :
        _setupPythonPath()
    main()
    

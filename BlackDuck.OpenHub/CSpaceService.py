#!/usr/bin/python
import os, sys

# The actual commandline entry point
from cspace.main.service import main
import cspace.ext.storefwd

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

if __name__ == '__main__' :
    if not hasattr(sys,'frozen') :
        _setupPythonPath()
    main()

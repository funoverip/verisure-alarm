#!/usr/bin/env python
#
# Convert Verisure node Name to node ID
# By Jerome Nokin (http://funoverip.net / @funoverip)
#

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from securitas_name_convert import id2name, name2id

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "Usage: %s <name>" % sys.argv[0]
        print "Ex:    %s '262E 9BV7'" % sys.argv[0]
        sys.exit(0)

    nodename = sys.argv[1]
    nodeid = name2id(nodename)

    print "Name: %s" % nodename
    print "Id  : %08x" % nodeid

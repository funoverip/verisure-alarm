#!/usr/bin/env python
#
# Convert Verisure node ID to node Name
# By Jerome Nokin (http://funoverip.net / @funoverip)
#


import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from securitas_name_convert import id2name, name2id

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "Usage: %s <id>" % sys.argv[0]
        print "Ex:    %s 0100c3a7" % sys.argv[0]
        sys.exit(0)

    nodeid = sys.argv[1]
    nodeid = int(nodeid, 16)

    nodename = id2name(nodeid)
    print "Id  : %08x" % nodeid
    print "Name: %s" % nodename

#!/usr/bin/env python
# 
# Parse Verisure Vbox memory (dumpfile) and search for personal crypt/hash keys
# By Jerome Nokin (http://funoverip.net / @funoverip)
#

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
import argparse
from binascii import hexlify, unhexlify
from securitas_name_convert import id2name, name2id, name2id_as_str


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nodename", help=" Vbox node Name (ex: '262D 3BF9')",  type=str , required=False)
    parser.add_argument("-i", "--nodeid", help="Vbox node ID (ex: '0100d37c')",  type=str , required=False)
    parser.add_argument("-f", "--file", help="Memory dump file",  type=str , required=True)
    args = parser.parse_args()


    # Testing node args
    vbox_id_as_str=''
    vbox_id=0
    vbox_name=''
    if not (args.nodename or args.nodeid) or (args.nodename and args.nodeid):
        print "Error. You must provide the name (-n) OR the id (-i) of your Vbox"
        sys.exit(0)
    
    if args.nodeid:
        vbox_id_as_str = unhexlify(args.nodeid)
        vbox_id_as_str = vbox_id_as_str[3] + vbox_id_as_str[2] + vbox_id_as_str[1] + vbox_id_as_str[0]
        vbox_id = long(args.nodeid, 16)
        vbox_name = id2name(vbox_id)

    if args.nodename:
        vbox_name = args.nodename
        vbox_id = name2id(vbox_name)
        vbox_id_as_str = name2id_as_str(vbox_name)
        vbox_id_as_str = vbox_id_as_str[3] + vbox_id_as_str[2] + vbox_id_as_str[1] + vbox_id_as_str[0]


    # Testing dumpfile arg
    dumpfile = args.file
    try:
        dumpfile_size = os.path.getsize(dumpfile)
    except:
        print "ERROR while opening %s" % dumpfile
        sys.exit(0)


    print "[*] Provided arguments:"
    print "    Dumpfile     : %s" % dumpfile
    print "    Dumpfile size: %d bytes" % dumpfile_size
    print "    Vbox name    : %s" % vbox_name
    print "    Vbox id      : %08x" % vbox_id

    print "[*] Searching memory..."

    with open(dumpfile, "rb") as f:
        mem = f.read()


    i =0
    found_device_list = False
    while i <= dumpfile_size-4:

        # Searching VBOX id
        #===================
        found_vbox = False
        while True:
            if i >= dumpfile_size-4:
                break
            if mem[i:i+4] == vbox_id_as_str:
                print "    Potential device list was found.. ",
                found_vbox = True
                break
            i+=1


        # Found it? Then get keys
        #========================
        if found_vbox:
            device_id = mem[i:i+4]
            i+=4
            # Do we have 32 null free byte + \x00 or \x02 ?
            if not '\x00' in mem[i:i+32] and (mem[i+32] == '\x00' or mem[i+32] == '\x02'):

                print "=> Confirmed!"
                print "[*] Extracting device list and crypto keys"

                found_device_list = True
                key_crypt = ' '.join(hexlify(n) for n in mem[i:i+16])
                key_hash  = ' '.join(hexlify(n) for n in mem[i+16:i+32])
                print "    Device  : %s (VBOX!) " % hexlify(device_id[3] + device_id[2] + device_id[1] + device_id[0])
                print "       crypt: %s" % key_crypt if len(key_crypt) == 47 else "  crypt: %s <INCOMPLETE>" % key_crypt
                print "       hash : %s" % key_hash  if len(key_hash)  == 47 else "  hash : %s <INCOMPLETE>" % key_hash
                i+=32 # keys space
                i+=1  # ending byte

                # Searching for other device/keys
                for j in range(0,63):
                    if i >= dumpfile_size-4:
                        break
                    device_id    = mem[i:i+4]
                    i+=4
                    key_crypt = ' '.join(hexlify(n) for n in mem[i:i+16])
                    i+=16
                    key_hash  = ' '.join(hexlify(n) for n in mem[i:i+16])
                    i+=16
                    i+=1
    
                    if not device_id == '\x00\x00\x00\x00':
                        print "    Device  : %s" % hexlify(device_id[3] + device_id[2] + device_id[1] + device_id[0])
                        print "       crypt: %s" % key_crypt if len(key_crypt) == 47 else "  crypt: %s <INCOMPLETE>" % key_crypt
                        print "       hash : %s" % key_hash  if len(key_hash)  == 47 else "  hash : %s <INCOMPLETE>" % key_hash

                print "[*] Done"
                break


            # We do NOT have 32 null free byte + (\x00 or \x02)
            else:
                print "=> False positive"
        else:
            print "[-] VBox not found in dumpfile"
            break

    sys.exit(0)


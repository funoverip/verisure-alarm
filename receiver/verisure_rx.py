#!/usr/bin/env python
#=============================================================
# Securitas-Direct (Verisure) RF sniffer
# By Jerome Nokin (http://funoverip.net / @funoverip)
#=============================================================
#
# Usage: securitas_rx.py [-k KEY]
#
# optional arguments:
#       -k,--key <KEY>     Optional AES-128 Key (hexadecimal)
#
#=============================================================

import ctypes
import sys
import datetime
import argparse
from grc.verisure_demod     import verisure_demod
from threading              import Thread
from Crypto.Cipher          import AES
from binascii               import hexlify, unhexlify
from time                   import sleep

# Colors
def pink(t):	return '\033[95m' + t + '\033[0m'
def blue(t): 	return '\033[94m' + t + '\033[0m'
def yellow(t): 	return '\033[93m' + t + '\033[0m'
def green(t): 	return '\033[92m' + t + '\033[0m'
def red(t): 	return '\033[91m' + t + '\033[0m'


# Thread dedicated to GNU Radio flowgraph
class flowgraph_thread(Thread):
    def __init__(self, flowgraph):
        Thread.__init__(self)
        self.setDaemon(1)
        self._flowgraph = flowgraph

    def run(self):
        self._flowgraph.Run()
	#print "FFT Closed/Killed"

# AES decryption
BS    = 16
pad   = lambda s : s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]
def aes_decrypt(ciphertext, iv, key, padding=True):
	
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if padding:
        return unpad(plaintext)
    else:
        return plaintext



# Generate timestamp
def get_time():
    current_time = datetime.datetime.now().time()
    return current_time.isoformat()

# Print out frames to stdout
def dump_frame(frame, aes_iv = None, aes_key = None):

    # Dissecting frame
    pkt_len = hexlify(frame[0:1])
    unkn1   = hexlify(frame[1:2])
    seqnr	= hexlify(frame[2:3])
    src_id	= "".join(hexlify(n) for n in frame[3:7])
    dst_id	= "".join(hexlify(n) for n in frame[7:11])
    data	= ""

    # Payload is a block of 16b and AES key provided ? Try to decrypt it
    if  (ord(unhexlify(pkt_len))-2-8) % 16 == 0 and aes_iv!=None and aes_key!=None:
        if unkn1 == '\x04':
            # block is 16b without additional padding
            data    = " ".join(hexlify(n) for n in aes_decrypt(frame[11:], aes_iv, aes_key, False))	
        else:
            # block is 16b with padding
            data	= " ".join(hexlify(n) for n in aes_decrypt(frame[11:], aes_iv, aes_key))
        if len(data) ==0:
            data = "<empty> Wrong EAS key ?"
    else:
        data 	= " ".join(hexlify(n) for n in frame[11:])

    # Print out the frame 
    print "[%s] %s %s %s %s %s %s" % (get_time(), yellow(pkt_len), blue(unkn1), seqnr, green(src_id), red(dst_id), pink(data))


# Main entry point
if __name__ == '__main__':

    aes_iv  = unhexlify("00000000000000000000000000000000")
    aes_key = None

    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
		
    # Read args
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", help="Optional AES-128 Key (hex)", type=str)
    args = parser.parse_args()

    # Initializing GNU Radio flowgraph
    flowgraph = verisure_demod()

    if args.key:
        print "[%s] AES key provided. Decryption enabled" % get_time()
        aes_key = args.key
        aes_key = ''.join(aes_key.split())
        aes_key = unhexlify(aes_key)
        print "[%s] AES-128 IV : %s" % (get_time(), hexlify(aes_iv))
        print "[%s] AES-128 key: %s" % (get_time(), hexlify(aes_key))

    # current frequency
    freq = 0
	
    # Some additional output
    print "[%s] Starting flowgraph" % get_time()
	
    # Start flowgraph insie a new thread
    flowgraph_t = flowgraph_thread(flowgraph)
    flowgraph_t.start()
	
    # Until flowgraph thread is running (and we hope 'producing')
    while flowgraph_t.isAlive():
        # Did we change frequency ?
        if freq != flowgraph.get_frequency():
            print "[%s] Frequency tuned to: %0.2f KHz" % (get_time(), flowgraph.get_frequency()/1000)
            freq = flowgraph.get_frequency()
			
        # Emptying message queue
        while True:
            if flowgraph.myqueue.count() <= 0:
                break;
            frame = flowgraph.myqueue.delete_head_nowait().to_string()
            dump_frame(frame, aes_iv, aes_key)

        # I can't exit the script because of a blocking call to "myqueue.delete_head()". So for now..
        sleep(0.1)
		
    print "[%s] Exiting" % (get_time())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


import numpy as np
from struct import pack, unpack

word_8736E =    "\x00\x01\x02\x03\x04\x05\x06\x07\xff\xff\xff\xff\xff\xff\xff" + \
                "\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\xff\x10\x11\x12\x13\x14\xff" + \
                "\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"

unk_87397 =     "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"

def id2name(id):
    global unk_87397

    tmp = id >> 24

    result = ((id << 8) | (((id >> 16) ^ (id >> 8) ^ id ^ (id >> 24)) & 0xFF)) & 0xffffffff
    ret = ''

    for i in reversed(range(0,9)):

        if i == 4:
            ret = ' ' + ret
        else:
            ret = unk_87397[result & 0x1F] + ret
            result = (result >> 5) | (tmp << 27)
            tmp >>= 5

    return ret

def name2id(name):

    global word_8736E

    i = np.int32(0)
    j = i
    result = np.int64(0)

    while True:
        if i > j + 7:
            return np.int32(result >> 8)
        c = np.uint8(ord(name[i]))
        if c == np.uint8(ord(' ')):
            j += 1
        else:
            tmp = word_8736E[c - 50]
            if ord(tmp) == 255:
                return 0
            v10 = np.uint32(result >> 27)
            result_lo = np.uint32(np.uint32(ord(tmp) & 0x1F) | np.int64(32 * np.uint32(result)))
            result_hi = v10 | (32 * (result >> 32))
            result = np.int64( (result_hi << 32) | result_lo  )
            
        i += 1

def name2id_as_str(name):
    return pack(">I",name2id(name))

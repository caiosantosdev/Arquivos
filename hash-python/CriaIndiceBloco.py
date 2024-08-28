import hashlib
import os
import ctypes
import struct

fileName = "data/cep.dat"
indexName = "data/cep-hash-bloco.dat"
N = 1000
hashSize = 1399
dataFormat = "72s72s72s72s2s8s2s"
dataStruct = struct.Struct(dataFormat)
keyColumnIndex = 5

class HashPage(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint16),
        ("keys", ctypes.c_uint32 * N), 
        ("pointers", ctypes.c_uint32 * N),
        ("next", ctypes.c_uint32)
    ]

def h(key):
    return key%hashSize

hp = HashPage()
with open(indexName,"wb") as fi:
    for i in range(0,hashSize):
        fi.write(hp)

f = open(fileName,"rb")
fi = open(indexName,"r+b")
fi.seek(0,os.SEEK_END)
fileIndexSize = fi.tell()
recordNumber = 0
while True:
    line = f.read(dataStruct.size)
    if len(line) == 0: # EOF
        break
    record = dataStruct.unpack(line)
    key = int(record[keyColumnIndex]) 
    p = h(key)
    fi.seek(p*ctypes.sizeof(hp),os.SEEK_SET)
    fi.readinto(hp)
    fi.seek(p*ctypes.sizeof(hp),os.SEEK_SET)
    if(hp.size < N):
        hp.keys[hp.size] = key
        hp.pointers[hp.size] = recordNumber
        hp.size += 1
        fi.write(hp)
    else:
        print(key)        
    recordNumber += 1
f.close()
fi.close()


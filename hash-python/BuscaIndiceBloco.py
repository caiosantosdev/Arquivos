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


f = open(fileName,"rb")
fi = open(indexName,"rb")

hp = HashPage()
cep = 22755170
p = h(cep)
fi.seek(p*ctypes.sizeof(hp),os.SEEK_SET)
fi.readinto(hp)

for i in range(hp.size):
    if(hp.keys[i]==cep):
        pos = hp.pointers[i]
        print(f"Achei o cep {cep} posicao {pos}")
        f.seek(pos*dataStruct.size)
        print(f.read(dataStruct.size))
fi.close()
f.close()


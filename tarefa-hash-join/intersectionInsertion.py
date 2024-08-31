import struct
import os
import ctypes

hashTableFileName = 'data/hashTable'

N = 1000
hashSize = 1200
dataFormat = "72s72s72s72s2s8s2s"
dataStruct = struct.Struct(dataFormat)
cepColumnIndex = 5

class HashPage(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint16),
        ("keys", ctypes.c_uint32 * N), 
        ("pointers", ctypes.c_uint32 * N),
        ("next", ctypes.c_uint32)
    ]

def h(key):
    return key % hashSize

def intersection(arqOne, arqTwo):
    f3 = open("data/intersection.dat", "wb")
    hashF1 = open(arqOne, "rb")
    hashPage = HashPage()

    f2 = open(arqTwo, "rb")

    while True:
        line = f2.read(dataStruct.size)
        if len(line) == 0:
            break

        record = dataStruct.unpack(line)
        key = int(record[cepColumnIndex])
        p = h(key)

        hashF1.seek(p * ctypes.sizeof(hashPage), os.SEEK_SET)
        hashF1.readinto(hashPage)

        # Verifica se a chave existe na tabela de hash
        for j in range(hashPage.size):
            if hashPage.keys[j] == key:
                # Se a chave for encontrada, escreve o registro no arquivo de interseção
                f3.write(line)
                break

    hashF1.close()
    f2.close()
    f3.close()

# Chama a função de interseção
intersection("./data/hashTableOne.dat", "./data/randomTwo.dat")


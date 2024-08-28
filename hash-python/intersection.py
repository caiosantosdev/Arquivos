# dado dois arquivos, ler o primeiro e criar uma tabela de hash conforma feito em sala de aula.
# cada posicao da tabela de hash tem 1000 ponteiros para registros da tabela cep.
# para cada chave do primeiro arquivo, faca um hash para verificar em qual posicao da tabela ele vai ser armazenado
# insira a chave no bloco correspondente
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
    return key%hashSize
#



def Verifica(index1, index2):
    
    inFileOne = open(index1, 'r+b')
    inFileTwo = open(index2, 'r+b')
    c = open("data/saida.dat", 'wb')
    arq = open("data/randomOne.dat", "rb")
    hashPageOne = HashPage()
    hashPageTwo = HashPage()
    inFileOne.seek(0,os.SEEK_END)
    inFileTwo.seek(0,os.SEEK_END)
    arq1Size = inFileOne.tell()
    arq2Size = inFileTwo.tell()
    line = inFileOne.read(dataStruct.size)
    # if len(line) == 0: # EOF
    #     return False
    # record = dataStruct.unpack(line)
    # key = int(record[keyColumnIndex]) 
    if arq1Size != arq2Size:
        print("Os arquivos possuem tamanhos diferentes")
        return False
    inFileOne.seek(0)
    inFileTwo.seek(0)
    for i in range(hashSize):
        inFileOne.readinto(hashPageOne)
        for j in range(hashPageOne.size):
            inFileTwo.seek(i*ctypes.sizeof(HashPage),os.SEEK_SET)
            inFileTwo.readinto(hashPageTwo)
            for k in range (hashPageTwo.size):
                if hashPageOne.keys[j] == hashPageTwo.keys[k]:
                    arq.seek(hashPageOne.pointers[j]*dataStruct.size,os.SEEK_SET)
                    c.write(arq.read(dataStruct.size))
                    break

    inFileOne.close()
    inFileTwo.close()
    c.close()
    arq.close()

hashTableOne = "./data/hashTableOne.dat"
hashTableTwo = "./data/hashTableTwo.dat"

Verifica(hashTableOne, hashTableTwo)
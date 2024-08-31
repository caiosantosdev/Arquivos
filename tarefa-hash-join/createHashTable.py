# dado dois arquivos, ler o primeiro e criar uma tabela de hash conforma feito em sala de aula.
# cada posicao da tabela de hash tem 1000 ponteiros para registros da tabela cep.
# para cada chave do primeiro arquivo, faca um hash para verificar em qual posicao da tabela ele vai ser armazenado
# insira a chave no bloco correspondente
import struct
import os
import ctypes

inFileOne = 'data/randomOne.dat'
inFileTwo = 'data/randomTwo.dat'

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
def createHashTable(inputFile, outputHashTableFileName):
    hp = HashPage()

    with open(outputHashTableFileName, "wb") as fi:
        for i in range(0, hashSize):
            fi.write(hp)


    f = open(inputFile, "rb")
    fi = open(outputHashTableFileName, "r+b")
    fi.seek(0,os.SEEK_END)
    fileOneSize = fi.tell()
    recordNumber = 0
    while True:
        line = f.read(dataStruct.size)
        if len(line) == 0:
            break
        # unpack na line para pegar o registro do cep e aplicar na função de hash
        record = dataStruct.unpack(line)
        key = int(record[cepColumnIndex])
        p = h(key)
        # Seek para a posição da tabela de hash
        fi.seek(p*ctypes.sizeof(hp), os.SEEK_SET)
        fi.readinto(hp)
        fi.seek(p*ctypes.sizeof(hp),os.SEEK_SET)
        # Verifica se ainda cabe chaves dentro da hashPage
        # Se couber, insere a chave na hashpash e escreve dentro da HashTable.
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

createHashTable(inFileOne, "data/hashTableOne.dat")

# createHashTable(inFileTwo, "data/hashTableTwo.dat")
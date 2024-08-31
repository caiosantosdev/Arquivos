# 
import random as random
import struct

dataFormat = "72s72s72s72s2s8s2s"
dataStruct = struct.Struct(dataFormat)

def extracaoAleatoria(fileName, outFileName):
    inFile = open(fileName, "rb")
    outFile = open(outFileName, "wb")
    while True:
        # Le uma linha do arquivo original.
        line = inFile.read(dataStruct.size)
        if len(line) == 0:
            break
        number = random.randint(0,1)
        if(number <= 0.8):
            outFile.write(line)
    print(f"arquivo '{outFileName}' gerado")
    
cep = 'data/cep.dat'
outFileOne = 'data/randomOne.dat'
outFileTwo = 'data/randomTwo.dat'

extracaoAleatoria(cep, outFileOne)
extracaoAleatoria(cep, outFileTwo)




# criar novo arquivo com 80% (0.8) dos arquivos do primeiro arquivos. ( A PARTIR DO CEP.DAT)
# ler arquivo 1 linha por 1 linha
# sortear numero de 0 a 9, se cair < 8, escrever no novo arquivo.
# fazer isso para todas as linhas.
# fazer isso duas vezes para gerar dois arquivos.


# f = open(arqEntrada, 'r')
# linhas = f.readlines()
# sugest: utilizar rb e wb para tornar arq binario
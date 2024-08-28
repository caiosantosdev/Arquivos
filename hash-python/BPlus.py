import os
import ctypes
import random

N = 512 # Page Size in Number Of Elements

class BPlusTreeFileManager:

    def __init__(self, filename):
        self.open(filename)
    
    def open(self, filename):
        if os.path.exists(filename):
            self.f = open(filename,"r+b")
            self.isNew = False
        else:
            self.f = open(filename,"w+b")
            self.isNew = True

    def close(self):
        self.f.close()
        self.f = None
        self.isNew = None

    def writeHeader(self, header):
        self.f.seek(0)
        self.f.write(header)
        return header

    def readHeader(self):
        buffer = BPlusTreeHeader()
        self.f.seek(0)
        self.f.readinto(buffer)
        return buffer

    def readPage(self, pageNumber, pageBuffer=None):
        if pageBuffer == None:
            pageBuffer = BPlusTreePage()
        self.f.seek(HEADER_SIZE+pageNumber*BPLUSTREE_PAGE_SIZE)
        self.f.readinto(pageBuffer)
        return pageBuffer
    
    def writePage(self, pageNumber, page):
        headerSize = ctypes.sizeof(BPlusTreeHeader)
        pageSize = ctypes.sizeof(BPlusTreePage)
        offset = headerSize + pageNumber * pageSize
        self.f.seek(offset)
        self.f.write(page)
        return page

    def appendPage(self, page):
        self.f.seek(0,os.SEEK_END)
        offset = self.f.tell()
        self.f.write(page)
        headerSize = ctypes.sizeof(BPlusTreeHeader)
        pageSize = ctypes.sizeof(BPlusTreePage)
        return (offset-headerSize)//pageSize

    def fileSize(self):
        self.f.seek(0,os.SEEK_END)
        return self.f.tell()

    def pageCount(self):
        headerSize = ctypes.sizeof(BPlusTreeHeader)
        pageSize = ctypes.sizeof(BPlusTreePage)
        return (self.fileSize()-headerSize)//pageSize

class BPlusTreeHeader(ctypes.Structure):
    _fields_ = [
        ("height", ctypes.c_uint8), # the height of tree
        ("size", ctypes.c_uint32), # size (number of elements)
        ("leftmostLeaf", ctypes.c_uint32) # (pointer to leftmost leaf page)
    ]

HEADER_SIZE = ctypes.sizeof(BPlusTreeHeader)

class BPlusTreePage(ctypes.Structure):
    _fields_ = [
        ("isLeaf", ctypes.c_bool), # indicates if page is leaf or not
        ("size", ctypes.c_uint16), # indicetes how many keys are there in pages
        ("keys", ctypes.c_uint32 * N), # array of PAGESIZE integer keys
        ("pointers", ctypes.c_uint32 * (N+1)) # array of PAGESIZE+1 pointers
    ]

    def simpleInsertSort(self, key, pointer):
        keys = self.keys
        pointers = self.pointers
        first = 0
        last = self.size-1
        while first <= last:
            pos = (first+last)//2
            if key < keys[pos]:
                last = pos-1
            else:
                first = pos+1
        last += 1
        src = ctypes.addressof(keys)+(last)*4
        c = (self.size-(last))*4
        ctypes.memmove(src+4,src,c)
        src = ctypes.addressof(pointers)+(last+1)*4
        ctypes.memmove(src+4,src,c)
        keys[last] = key
        pointers[last+1] = pointer
        self.size += 1

    # def simpleInsertSort(self, key, pointer):
    #     keys = self.keys
    #     pointers = self.pointers
    #     keys[self.size] = key
    #     pointers[self.size+1] = pointer
    #     i = self.size
    #     while i > 0 and keys[i] < keys[i-1]:
    #         aux = keys[i]
    #         keys[i] = keys[i-1]
    #         keys[i-1] = aux
    #         aux = pointers[i+1]
    #         pointers[i+1] = pointers[i]
    #         pointers[i] = aux
    #         i -= 1
    #     self.size += 1

    def insert(self, key, pointer):
        if self.size < len(self.keys):
            self.simpleInsertSort(key,pointer)
            return None

        splitPage = BPlusTreePage()
        splitPage.isLeaf = self.isLeaf
        splitPage.size = (len(self.keys)+1)//2
        if key < self.keys[-1]:
            splitPage.keys[splitPage.size-1] = self.keys[-1]
            splitPage.pointers[splitPage.size] = self.pointers[-1]
            self.size -= 1
            self.simpleInsertSort(key,pointer)
        else:
            splitPage.keys[splitPage.size-1] = key
            splitPage.pointers[splitPage.size] = pointer
        i = self.size-1; j = splitPage.size-2
        while j >= 0:
            splitPage.keys[j] = self.keys[i]
            splitPage.pointers[j+1] = self.pointers[i+1]
            self.keys[i] = 0
            self.pointers[i+1] = 0
            i -= 1; j-= 1
        self.size = i+1
        if self.isLeaf:
            splitPage.pointers[0] = self.pointers[0]
        else:
            splitPage.pointers[0] = self.pointers[self.size]
            self.pointers[self.size] = 0
        return splitPage

    def printDebug(self):
        print(f"|{self.size:05d}{'*' if self.isLeaf else ' '}|",end="")
        print(f"<{self.pointers[0]:05x}>",end="")
        for i in range(len(self.keys)):
            print(f" ({self.keys[i]:06d}) ",end="")
            print(f"<{self.pointers[i+1]:05x}>",end="")
        print()

BPLUSTREE_PAGE_SIZE = ctypes.sizeof(BPlusTreePage)


class BPlusTree:

    def __init__(self, filename="btree.dat"):
        self.f = BPlusTreeFileManager(filename)
        if self.f.isNew:
            self.header = BPlusTreeHeader()
            self.header.height = 1
            self.header.size = 0
            self.header.leftmostLeaf = 0
            self.f.writeHeader(self.header)
            self.root = BPlusTreePage()
            self.root.isLeaf = True
            self.f.writePage(0,self.root)
        else:
            self.header = self.f.readHeader()
            self.root = self.f.readPage(0)

    def __insertInPage(self, page, pageNumber, key, pointer):
        splitKey = None
        splitPointer = None
        splitPage = page.insert(key,pointer)
        if splitPage != None:
            splitPointer = self.f.appendPage(splitPage)
            if page.isLeaf:
                page.pointers[0] = splitPointer
                splitKey = splitPage.keys[0]
            else:
                page.size -= 1
                splitKey = page.keys[page.size]
                page.keys[page.size] = 0
        self.f.writePage(pageNumber, page)
        return splitKey, splitPointer 

    def __recursiveInsert(self, offset, page, key, pointer):
        if page.isLeaf:
            return self.__insertInPage(page, offset, key, pointer)
        j = page.size
        for i in range(page.size):
            if key < page.keys[i]:
                j = i
                break
        childrenOffset = page.pointers[j]
        childrenPage = self.f.readPage(childrenOffset)
        childrenSplitKey, childrenSplitPointer = self.__recursiveInsert(childrenOffset, childrenPage, key, pointer)
        if childrenSplitKey != None:
            return self.__insertInPage(page, offset, childrenSplitKey, childrenSplitPointer)
        return None, None

    def insert(self, key, pointer):
        splitKey, splitPointer = self.__recursiveInsert(0, self.root, key, pointer)
        if splitKey != None:
            self.header.height += 1
            leftPointer = self.f.appendPage(self.root)
            self.root = BPlusTreePage()
            self.root.keys[0] = splitKey
            self.root.pointers[0] = leftPointer
            self.root.pointers[1] = splitPointer
            self.root.size = 1
            self.root.isLeaf = False
            self.f.writePage(0,self.root)
            if self.header.leftmostLeaf == 0:
                self.header.leftmostLeaf = leftPointer
        self.header.size += 1

    def search(self, key):
        currentPage = self.root
        while True:
            i = j = 0
            while i < currentPage.size and key >= currentPage.keys[i]:
                i += 1
                j = i
            if currentPage.isLeaf:
                if currentPage.keys[j-1] == key:
                    return currentPage.pointers[j]
                else:
                    return None
            currentPage = self.f.readPage(currentPage.pointers[j])
 
    def printDebug(self):
        p = BPlusTreePage()
        for i in range(self.f.pageCount()):
            self.f.readPage(i,p)
            print(f"{i:05d}  ",end="")
            p.printDebug()

    def close(self):
        self.f.writeHeader(self.header)
        self.f.close()

def runTest():
    a = BPlusTree()
    values = [*range(1000000, 2000000)]
    random.shuffle(values)
    for v in values:
        a.insert(v,0xB0DE)
    # for v in values:
    #     pos = a.search(v)
    #     if pos == None:
    #         print (f"PERDEU {v} na posicao {i}")
    #         break

    # a.printDebug()
    a.close()


runTest()

#    print(f"Inserindo {v} - {a.header.height}")
    # for j in range(i+1):
    #     pos = a.search(values[j])
    #     if pos == None:
    #         print (f"PERDEU {values[i]}")
    #         erro = True
    #         break
    # if erro: break
#a.printDebug()
# for i,v in enumerate(values):
#     pos = a.search(v)
#     if pos == None:
#         print (f"PERDEU {v} na posicao {i}")
#         break
# a.printDebug()
# a.close()


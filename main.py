from os import listdir
from os.path import isfile, join
from itertools import combinations
import timeit
import hashlib, zlib, mmh3, xxhash

class Hash():
    def __init__(self, funcao_hash):
        self.__funcao_hash = funcao_hash
        self.__qtd_colisoes = 0
        self.__hist = {}
        self.__colisoes = {}
        self.__tempos = {}
    
    def calcular_hash(self, codigo):
        tempo = timeit.timeit(lambda: self.__funcao_hash(codigo), number=1000, globals=globals())
        tam = len(codigo)
        if(tam in self.__tempos):
            self.__tempos[tam].append(tempo)
        else:
            self.__tempos[tam] = [tempo]

        hash = self.__funcao_hash(codigo)
        if(hash in self.__hist):
            if(hash in self.__colisoes):
                self.__colisoes[hash].append(codigo)
            else:
                self.__colisoes[hash] = [codigo, self.__hist[hash]]
            self.__qtd_colisoes += 1
        self.__hist[hash] = codigo
        
        return tempo, hash

    def salvar_dados(self, filename):
        with open(filename, "w") as arq:
            arq.write("Tempos: {0}\n\n".format(self.__tempos))
            arq.write("Histórico: {0}\n\n".format(self.__hist))
            arq.write("Colisões: {0}\n\n".format(self.__colisoes))
            arq.write("Qtd Colisões: {0}".format(self.__qtd_colisoes))
    
    @property
    def tempos(self):
        return self.__tempos
    
    @property
    def qtd_colisoes(self):
        return self.__qtd_colisoes

    @property
    def hist(self):
        return self.__hist

    @property
    def colisoes(self):
        return self.__colisoes

def hash_djb2(s):                                                                                                                                
    hash = 5381
    for x in s:
        hash = (( hash << 5) + hash) + ord(x)
    return hash & 0xFFFFFFFF

def f_crc32(codigo):
    return hex(zlib.crc32(codigo.encode('utf')))

def f_murmur(codigo):
    return mmh3.hash_bytes(codigo.encode('utf')).hex()

def f_djb2(codigo):
    return hex(hash_djb2(codigo))

def f_xxhash(codigo):
    return xxhash.xxh128_hexdigest(codigo.encode('utf'))

def f_md5(codigo):
    return hashlib.md5(codigo.encode('utf')).hexdigest()

h_crc32 = Hash(f_crc32)   #CRC32
h_murmur = Hash(f_murmur) #MURMUR
h_djb2 = Hash(f_djb2)     #DJB2
h_xxhash = Hash(f_xxhash) #XXHASH
h_md5 = Hash(f_md5)       #MD5

#Obtendo os códigos das funções que calcularemos o hash
funcoes = []
arquivos = [join("entrada", f) for f in listdir("entrada") if isfile(join("entrada", f))]
for arq in arquivos:
    with open(arq, "r") as a:
        func = ""
        for linha in a.readlines():
            if(linha.startswith("def ")):
                funcoes.append(func)
                func = ""
            else:
                func += linha

print(len(funcoes))

###################funcoes = ["a", "b", "c"]

#Realizando todas as combinações possíveis com a funções da entrada
#e gerando os hashes dessas combinações.

j = 0

for i in range(1, len(funcoes)+1):
    for combin in combinations(funcoes, i):
        codigo = "".join(combin)
        h_crc32.calcular_hash(codigo)
        h_murmur.calcular_hash(codigo)
        h_djb2.calcular_hash(codigo)
        h_xxhash.calcular_hash(codigo)
        h_md5.calcular_hash(codigo)

        ####################print(codigo)
        j += 1
        print(j)
    if(j == 104): break

h_crc32.salvar_dados("saida/CRC32.txt")
h_murmur.salvar_dados("saida/MURMUR.txt")
h_djb2.salvar_dados("saida/DJB2.txt")
h_xxhash.salvar_dados("saida/XXHASH.txt")
h_md5.salvar_dados("saida/MD5.txt")


print(len(funcoes))
print(2**len(funcoes) - 1)
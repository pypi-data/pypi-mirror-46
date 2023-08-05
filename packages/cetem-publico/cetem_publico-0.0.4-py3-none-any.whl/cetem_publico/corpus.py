
import requests
import os
import re
import sys
from nltk.corpus.reader.conll import ConllCorpusReader


#escrever dados num ficheiro
#obter caminho do utilizador
home_path = os.environ['HOME']
#pasta para onde gravaremos os dados
folder = home_path + "/.cetem_publico"


#faz download de uma base de dados para um ficheiro
#TODO: colocar o ficheiro sobre forma de zip(provavelmente usando xz)
def download():
  #url do ficheiro, hardcoded por enquanto
  url = "http://bit.do/cetem2019"
  #fazer pedido da base de dados ao url especificado
  data = requests.get(url)
  #criar
  os.makedirs(folder,exist_ok=True)
  filename = folder +"/cetem_publico_10k.txt"
  open(filename,"wb").write(data.content)



#transforma o ficheiro cetem publico para ter formato conll
def cetem_to_conll(corpusFilename):
    file = open(corpusFilename)

    os.makedirs(folder  + '/conll/',exist_ok=True)

    ficheiro_atual = ""
    frase = False

    for line in file.readlines():
        #
        line = line.rstrip()
        #
        match = re.match(r'<ext n=(.*?) sec=(.*?) sem=(.*?)>$',line)
        #
        if match:
            #
            folder_to_write = folder + '/conll/' + match[2] +'/' + match[3] + '/'
            os.makedirs(folder_to_write,exist_ok=True)
            #
            file_name = match[1]+ '-' + match[2]+ '-'+match[3]+'.conll'
            #
            ficheiro_atual = open(folder_to_write + file_name,'w')
            continue
        #
        if re.match(r'<s>',line):
            frase = True
            continue
        #
        if re.match(r'</s>',line):
            frase = False
            ficheiro_atual.write('\n')
            continue
        #
        if re.match(r'</ext>',line):
            ficheiro_atual.close()
            continue
        #
        if re.match(r'</?mwe',line):
            continue
        #
        if frase:
            campos = line.split('\t')
            ficheiro_atual.write('\t'.join(campos)+ '\n')
            continue

#
def load_corpus():
  #
  if not os.path.exists(folder + "/cetem"):
    download()
  #
  filename = folder +"/cetem_publico_10k.txt"
  cetem_to_conll(filename)
  #
  load_to_nltk(folder  + '/conll/')
  #
  print("done processing corpus")
    

#
def load_to_nltk(folder):
    corpus = ConllCorpusReader(folder, \
                                r".*\.conll", \
                                ('words','ignore','ignore','ignore','pos'))
    print(corpus.tagged_sents())

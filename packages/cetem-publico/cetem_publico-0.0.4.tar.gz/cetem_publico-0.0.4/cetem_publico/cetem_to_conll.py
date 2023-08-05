import re
import sys
import os
import getopt

opts, args = getopt.getopt(sys.argv[1:], "")
opts = dict(opts)

#
def load_corpus(corpusFilename):
    file = open(corpusFilename)

    ficheiro_atual = ""
    frase = False

    for line in file.readlines():
        match = re.match(r'<ext n=(.*?) sec=(.*?) sem=(.*?)>$',line)
        if match:
            file_name = match[1]+ '-' + match[2]+ '-'+match[3]+'.conll'
            ficheiro_atual = open('conll/'+file_name,'w')
            continue
        
        if re.match(r'<s>',line):
            frase = True
            continue
        
        if re.match(r'</s>',line):
            frase = False
            continue

        if re.match(r'</ext>',line):
            ficheiro_atual.close()
            continue

        if re.match(r'</?mwe',line):
            continue

        if frase:
            campos = line.split('\t')
            ficheiro_atual.write('\t'.join(campos)+ '\n')
            continue


#
load_corpus(args[0])

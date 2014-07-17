# -*- coding: utf-8 -*-
import random
import MeCab
import re






if __name__ == "__main__":
    parseLog()

def parseLog():
    srcfilename = "log.txt"
    destfilename = "learnsrc.txt"
    f = open(srcfilename, "r")
    f2 = open(destfilename, "a")
    line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
    while line:
        m = re.search('「.+」',line)
        if not m == None:
            str = m.group().replace("「","").replace("」","")
            f2.write(str + "\n") # 引数の文字列をファイルに書き込む
        line = f.readline()
        f.close  
    f2.close()
 


#    print m

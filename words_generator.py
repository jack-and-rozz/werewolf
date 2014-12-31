
# -*- coding: utf-8 -*-
import random
import MeCab
import sys,os

from utils import FilePath

sys.path.append(FilePath.ROOTPATH + "log_manager")

from log_parser import LogParser


class WordsGenerator():
    def __init__(self) :
        self.log_parser = LogParser()
        self.log_parser.loadParsedLog(FilePath.ROOTPATH + FilePath.PARSED_LOG)
        textlist = self.log_parser.outputAllTexts()
        self.wordlist = self.makeWordList(textlist)
        self.markov = self.makeMarkov()
        
    def makeWordList(self,textlist):
        t = MeCab.Tagger("-Owakati")
        wordlist = []
        for line in textlist:
            #一度に一定行数（10万くらい？超えると読み込めなくなってmがNoneになる
            m = t.parse(line).rstrip(" \n").split(" ") #split(" ")しないと空白含め1バイトずつ保存されてしまう 
            wordlist.extend(m)
        return wordlist
    def makeMarkov(self):
        markov = {}
        w1 = ""
        w2 = ""
        for word in self.wordlist:
            if w1 and w2:
                if (w1, w2) not in markov:
                    markov[(w1, w2)] = []
                markov[(w1, w2)].append(word)
            w1, w2 = w2, word
        return markov
    def makeSentence(self,l):
        # Generate Sentence
        count = 0
        sentence = ""
        w1, w2  = random.choice(self.markov.keys())
        while count < l:
            if not self.markov.has_key((w1,w2)):
                break
            tmp = random.choice(self.markov[(w1, w2)])
            sentence += tmp
            w1, w2 = w2, tmp
            count += 1
        return sentence




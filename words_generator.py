
# -*- coding: utf-8 -*-
import random
import MeCab
import sys,os

from werewolf_dictionary import FilePath

sys.path.append(FilePath.PATH + "log_manager")

from log_manager import LogManager


#とりあえず毎回学習。サイズが大きくなってくると学習結果を保存したほうが良さそう。
#これに加えて、何を言われたかもマルコフ遷移の条件にしなきゃダメそう。
#ログから、誰に対して何を言ったかを検出する。難しそう・・・

class WordsGenerator():
    def __init__(self) :
        self.log_manager = LogManager()
        self.log_manager.loadParsedLog(FilePath.PATH + FilePath.PARSED_LOG)
        texts = self.log_manager.outputAllTexts()
        self.wordlist = self.makeWordList(texts)
        self.markov = self.makeMarkov()
        for key in self.markov.keys():
            print key[0] + ","+key[1]
        
    def makeWordList(self,textlist):
        t = MeCab.Tagger("-Owakati")
        m = t.parse("私の名前はレトラです。")
        print len(m)
        print m
        exit()
        wordlist = []
        for line in textlist:
            #一度に一定行数（10万くらい？超えると読み込めなくなってmがNoneになる
            m = t.parse(line.rstrip("\n"))
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




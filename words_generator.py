
# -*- coding: utf-8 -*-
import random
import MeCab
import sys,os


#とりあえず毎回学習。サイズが大きくなってくると学習結果を保存したほうが良さそう。
#これに加えて、何を言われたかもマルコフ遷移の条件にしなきゃダメそう。
#ログから、誰に対して何を言ったかを検出する。難しそう・・・

class WordsGenerator():
    def __init__(self) :
        self.wordlist = self.makeWordList(os.path.dirname(os.path.abspath(__file__)) + "/log_analyzer/log_dest.txt")
        self.markov = self.makeMarkov()
    def makeWordList(self,filename):
        text = open(filename, "r").read()
        t = MeCab.Tagger("-Owakati")
        m = t.parse(text)
        #一定行数（10万くらい？超えると読み込めなくなってmがNoneになる
        result = m.rstrip(" \n").split(" ")
        return result
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
            tmp = random.choice(self.markov[(w1, w2)])
            sentence += tmp
            w1, w2 = w2, tmp
            count += 1
        return sentence




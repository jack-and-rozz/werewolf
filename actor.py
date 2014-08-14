# coding:utf-8

import random
from werewolf_dictionary import Const
from words_generator import WordsGenerator
from brain import Brain
from roles import Villager
from roles import Wolf
from roles import Lunatic
from roles import Seer
from roles import Medium
from roles import Hunter
from roles import Freemason

"""
Actorの思考にはなんのパラメータが必要か？

まず各役職について、誰がそうだと思っているか。役職の合計人数*100の配分でその度合いを表そうか。

"""


#職業に関係ないプレイヤーとしての情報を扱う。

class Actor:
    shared_word_generator = WordsGenerator() #とりあえず話し方は共有。
    def __init__(self,id,name,role_id,village):
        #アクターの不変の情報
        self.id = id
        self.name = name
        self.village = village #ここから現在の村の情報にアクセスする
        self.role = self.setRole(role_id)
        #アクターの現在の状態
        self.is_living = True
        #アクターの脳内。
        self.brain = Brain(self.village)
        #アクターのパラメータ・個性
        self.intelligence = 100
        self.words_generator = Actor.shared_word_generator
    def thinkInit(self):
        self.brain.initThinking()
        self.know((Const.Self,self.name),Const.RULE)
        self.know((Const.Self,self.role.name),Const.TRUTH)

        self.know((Const.TotalWolves,len(self.village.wolves)),Const.RULE)
   
        self.printAllInference()
    def printAllInference(self):
        print "< " + self.name + " >"
        for inf in self.brain.inference:
            print "%sは%sだ。　信頼性 %d " % (str(inf[0]),str(inf[1]),self.brain.inference[inf])
    def know(self,fact_tuple,reliability):
        self.brain.getKnowledge(fact_tuple,reliability)
    def speak(self):
        words = self.words_generator.makeSentence(20)
        print str(self.name) + " : " + words 
        self.village.addToChatlogs(self.id,words)
    def think(self):
        return
    def hear(self):
        return 
    def vote(self):
        vote_for = self.decideVoteTarget()
        return vote_for
    def decideVoteTarget(self):
        r = random.randint(0,len(self.village.livingActors())-1)
        i = self.village.livingActors()[r].id
        return self.village.actors[i].id

    def setRole(self,role_id): #役職インスタンスは自分がどのアクターなのかを知っている。
        if role_id == Const.Villager:
            return Villager(self.id,self.village)
        elif role_id == Const.Wolf:
            return Wolf(self.id,self.village)
        elif role_id == Const.Lunatic:
            return Lunatic(self.id,self.village)
        elif role_id == Const.Seer:
            return Seer(self.id,self.village)
        elif role_id == Const.Medium:
            return Medium(self.id,self.village)
        elif role_id == Const.Hunter:
            return Hunter(self.id,self.village)
        elif role_id == Const.Freemason:
            return Freemason(self.id,self.village)
        elif role_id == Const.Fox:
            return Fox(self.id,self.village)
        

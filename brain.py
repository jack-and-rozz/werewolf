# coding:utf-8
from werewolf_dictionary import Const



class Brain():
    def __init__(self,village):
        self.village = village
        self.suspicions = [[],[],[],[],[],[],[],[]] #各役職であると疑っている度合い?

        self.inference = {} 
    def searchInference(self):
        
        return

    def initThinking(self):
        actors_n = len(self.village.actors)
        wolves_n = len(self.village.wolves)
        for i in range(0,actors_n): #リストの初期化
            self.suspicions[Const.Wolf].append(0)
            self.suspicions[Const.Lunatic].append(0)
            self.suspicions[Const.Seer].append(0)
            self.suspicions[Const.Medium].append(0)
            self.suspicions[Const.Hunter].append(0)
            self.suspicions[Const.Freemason].append(0)
            self.suspicions[Const.Fox].append(0)
    def getKnowledge(self,fact,reliability):
        if not self.inference.has_key(fact):
            self.inference[fact] = reliability
            return True
        else: 
            if self.inference[fact] == Const.TRUTH or self.inference[fact] == Const.RULE  :  #TRUTH,NEVER,RULEは変更されない
                return False
            elif self.inference[fact] == Const.NEVER:
                return False
            else :
                self.inference[fact] = reliability
                return True
    def whatisA(b): #あるBに対してAを求める
        self.searchInferenceKey(1,b)
    def whatisB(a):
        self.searchInferenceKey(0,a)
    def searchInferenceKey(index,word):
        list = []
        t = self.inference
        if index == 0:
            for key in t.keys() : 
                if key[index] == word:
                    list.append(key[1])
        else:
            for key in t.keys() : 
                if key[index] == word:
                    list.append(key[0])
        return list


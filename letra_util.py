# coding:utf-8
import random
from werewolf_dictionary import Const

"""
ベクトル同士の内積のノルムが0になるのは正規化時
スカラと掛けるなら合計が1でいい
"""

class LetraWerewolfUtil:
    import random
    @classmethod
    def makeRandomName(self):
        a = random.randint(0,len(Const.ActorNameListA)-1)
        b = random.randint(0,len(Const.ActorNameListB)-1)
        return Const.ActorNameListA[a] + Const.ActorNameListB[b]
    @classmethod
    def makeDefaultName(self,i):
        return Const.ActorNameListA[i] + Const.ActorNameListB[i]
    @classmethod
    def totalOne(self,list):
        s = sum(list)
        for i in range(len(list)):
            list[i] =  1.0 * list[i]/ s
        return list

    

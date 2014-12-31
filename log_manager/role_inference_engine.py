# coding: utf-8
import random,math,re
import MeCab
import sys,os
import codecs


from utils import Const
from utils import FilePath


class RoleInferenceEngine():
    def __init__(self):
        self.evaluation = {} #各形態素毎の役職である可能性のスコア。 cf : self.evaluation["占い"] = [1.22,0.34,1.55,...] 
        self.roleList = Const.RoleNameWords.values()
        self.roleSuspection = {}
        for j in self.roleList:
            self.roleSuspection[j] = 0.0
         
    def loadLearnedParameters(self,srcfilename = FilePath.ROOTPATH + FilePath.ROLE_EVALUATION):
        f = open(srcfilename,"r")
        line = f.readline()
        name = ""
        character = None
        while line:
            m = re.search('(.+):([0-9]+\.[0-9]+),([0-9]+\.[0-9]+),([0-9]+\.[0-9]+),([0-9]+\.[0-9]+),([0-9]+\.[0-9]+),([0-9]+\.[0-9]+),([0-9]+\.[0-9]+),([0-9]+\.[0-9]+)',line)
            if m:
                morpheme = m.group(1)
                h = {}
                i = 2
                for j in self.roleList:
                    h[j] = float(m.group(i))
                    i += 1 
                self.evaluation[morpheme] = h
            line = f.readline()
        f.close()
    def roleDistinction(self,text):
        t = MeCab.Tagger("-Owakati")
        m = t.parse(text)
        result = m.rstrip(" \n").split(" ")
        for morpheme in result:
            if self.evaluation.has_key(morpheme):
                for j in self.roleList:
                    self.roleSuspection[j] += self.evaluation[morpheme][j] 
        max = 0
        role = None
        for j in self.roleSuspection.keys():
            if self.roleSuspection[j] >= max:
                max = self.roleSuspection[j]
                role = j
        return role
    
    def roleInferenceTest(self,rolename = "wolf"): 
        srcfilename = FilePath.ROOTPATH  + FilePath.SAMPLE_TEXTS+ "/text_" + rolename +""
        f = open(srcfilename, "r")
        line = f.readline() 
        role = None
        while line:
            if re.search(Const.CharacterDataLogFormat,line) == None:
                text = line
                role = self.roleDistinction(text)
                total = sum(self.roleSuspection.values())
                print role + " : " + str(self.roleSuspection[role] / total * 100) + "%"
            line = f.readline()
        f.close()       
        total = 0
        print "********************************************"
        print "<%s> 結果 : %s" % (rolename,role)
        for tp in self.roleSuspection.items():
            total += tp[1]
        for tp in self.roleSuspection.items():
            print ("%s  : %.3f %%")  % (tp[0], 100 * tp[1] / total)

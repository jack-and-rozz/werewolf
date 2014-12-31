# coding: utf-8 

import random,math,re
import MeCab
import sys,os
import codecs

from log_learning_engine import LogLearningEngine
from utils import Const
from utils import FilePath



#ソースファイルから整型したparsed_logの作成、parsed_logからの発言データの復元。
class LogParser():
    def __init__(self):
        self.log = {} #名前をキーとしたハッシュ。同名の別キャラクターも考慮し、キャラクタデータの配列characters[]を要素とする。
                      #characters[i]はlife,role,texts を要素として持つ。それぞれ、最終的な生存・役職・喋った台詞。

    def loadParsedLog(self,srcfilename = FilePath.ROOTPATH + FilePath.PARSED_LOG):
        f = open(srcfilename,"r")
        line = f.readline()
        name = ""
        character = None
        while line:
            m = re.search('\[(.*),(.*),(生存中|死亡)\]',line)
            if m == None:
                text = line
                character["texts"].append(text)
            else:
                #次のキャラクターが出てきたらself.logに追加
                if not character == None:
                    if not self.log.has_key(name):
                        self.log[name] = []
                    self.log[name].append(character)
                name = m.group(1)
                role = m.group(2)
                life = m.group(3)
                character = {"texts" : []}
                character["role"] = role
                character["life"] = life
            line = f.readline()
        if not self.log.has_key(name):
            self.log[name] = []
        self.log[name].append(character)
        f.close()
        
    #わかめてのログ用のパーサ。log_srcから整形したparsed_logを生成。
    def parseWakameteLog(self,srcfilename = FilePath.ROOTPATH  + "logfiles/log_src",characters = {}):
        f = open(srcfilename, "r")
        line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
        while line:
            #*****キャラクターデータ*****
            m = re.search('◆ 村人たち.+',line) #◆ 村人たち　から ◆ 出来事 までの間でキャラの情報がある
            if not m == None:
                line = f.readline() #一行読み飛ばす
                while(True):
                    line = f.readline() #キャラ名"
                    if not (re.search('出来事',line) == None):
                        break
                    else:
                        if re.search('.+',line).group(0).strip().replace("　","") == "":
                            line = f.readline() #たまに混じる空行を飛ばす
                        character_name = re.search('(.+)',line).group(1).strip().replace("　	","").replace("　","")
                        line = f.readline() #トリップ(飛ばす)
                        line = f.readline() #役職
                        while(re.search('\[(.+)\]',line) == None): #たまにトリップが
                            line = f.readline()
                        character_role = re.search('\[(.+)\]',line).group(1).strip().replace("　	","").replace("　","")
                        line = f.readline() #生存状況
                        character_life = re.search('（(.+)）',line).group(1).strip().replace("　	","").replace("　","")
                        idx = 0
                        if characters.has_key(character_name): 
                            characters[character_name].append({})
                            idx = len(characters[character_name]) - 1 #同名のキャラクタに備えてハッシュの配列にしておく
                        else:
                            characters[character_name] = [{}]
                        characters[character_name][idx]["role"] = character_role
                        characters[character_name][idx]["life"] = character_life
                        characters[character_name][idx]["texts"] = []
                     # characters : 名前をキーにして、職業・最終的な生存・喋った言葉　を持つハッシュ。同名の場合は配列に。
           
            #*****プレイヤーの台詞*****
            m = re.match('◆([^\s]+)?さん[^の念話]+\s*(「.*)?',line) 
            if not m == None :#192.168.20.2
                name = m.group(1).strip().replace("\t","").replace("　","").replace("　","")
                text = ""
                if not m.group(2) == None:
                    text = m.group(2).replace("「","").replace("」","")
                if characters.has_key(name) and not text == "": #仮で入って途中から名前変えた場合と、二行にまたがった発言は除く
                    idx = len(characters[name]) - 1 #同名のプレイヤーは基本的に最新のものを見続ける
                    characters[name][idx]["texts"].append(text)
            line = f.readline()
        f.close()
        return characters

    def getLog(self,srcfilename):
         self.parseWakameteLog(srcfilename,self.log)
       
    def saveParsedLog(self,destfilename = "log_manager/log_analyzer/parsed_log",option = "a"):
        f2 = open(destfilename, option)
        for name in self.log.keys():
            for character in self.log[name]:
                character_log  = "[%s,%s,%s]\n" % (name,character["role"],character["life"])
                f2.write(character_log)# 引数の文字列をファイルに書き込む 
                for text in character["texts"]:
                    f2.write(text + "\n") # 引数の文字列をファイルに書き込む 
        f2.close()
    def pickupCharactersHavingRole(self,role):
        players_list = [] 
        for name in self.log.keys():
            for character in self.log[name]: #同名キャラも考慮
                if character["role"] == role:
                    players_list.append(character)
        return players_list
    def outputAllTexts(self):
        textlist = []
        for characters in self.log.values():
            for character in characters:
                textlist.extend(character["texts"])
        return textlist

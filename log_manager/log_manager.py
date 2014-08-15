# coding: utf-8 

import random,math,re
import MeCab
import sys,os
import codecs

sys.path.append(os.pardir)
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/" + os.pardir)
#print os.pardir
#print os.path.dirname(os.path.abspath(__file__))
from werewolf_dictionary import Const
from werewolf_dictionary import FilePath

PATH = os.path.dirname(os.path.abspath(__file__)) + "/"


#パースしたログから学習したLogManagerインスタンスを元に、形態素毎の各役職のスコアを管理する。

class RoleInferenceEngine():
    def __init__(self,log):
        self.evaluation = {} #各形態素毎の役職である可能性のスコア。 cf : self.evaluation["占い"] = [1.22,0.34,1.55,...] 
        self.roleList = Const.RoleNameWords.values()
        self.counts = {}  #各形態素の登場回数
        self.speakNum = {} #各役職毎の発言(形態素)回数。
        self.log = log
        self.roleSuspection = {}
        for j in self.roleList:
            self.roleSuspection[j] = 0.0
            self.speakNum[j] = 0
    def learn(self,learn_srcfilename = PATH + "logfiles/parsed_log"):
        t = MeCab.Tagger("-Owakati")
        for role in Const.RoleNameWords.values():
            players = self.log.pickupCharactersHavingRole(role)
            for player in players:
                for text in player["texts"]:
                    m = t.parse(text)
                    result = m.rstrip(" \n").split(" ")
                    for morpheme in result:
                        self.addMorpheme(role,morpheme) #形態素を辞書に追加
        self.morphemeScoring()

    def addMorpheme(self,role,morpheme): #
        if not self.evaluation.has_key(morpheme):
            h = {}
            h2 = {}
            for j in self.roleList:
                h[j] = 0
                h2[j] = 0.0
            self.counts[morpheme] = h
            self.evaluation[morpheme] = h2
        self.speakNum[role] += 1
        self.counts[morpheme][role] += 1
    def morphemeScoring(self):
        for morpheme in self.evaluation.keys():
            c = sum(self.counts[morpheme].values()) * 1.0
            for j in self.roleList:
                if not self.speakNum[j] == 0:
                    #全員が良く言う言葉(役職名、挨拶)は頻度が当然高くなるので補正するため他の役職の発言数でも割る
                    CONST = 100 #自分の発言数をどこまで除くべきか？除かなくていいのか？とりあえず人狼がちゃんと人狼と判定されるとこまで。
                    c2 = c - self.counts[morpheme][j]/CONST if not c == self.counts[morpheme][j] else 1.0
                    s = 10**6 * self.counts[morpheme][j] / c2 / self.speakNum[j]
                    self.evaluation[morpheme][j] = s
        

    #評価値self.evaluationを元に
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
        srcfilename = PATH  + "sampletexts/text_" + rolename +""
        f = open(srcfilename, "r")
        line = f.readline() 
        role = None
        while line:
            if re.search(Const.CharacterDataLogFormat,line) == None:
                text = line
                role = self.roleDistinction(text)
                total = 0
                for i in self.roleSuspection.values() :
                    total +=  i
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
    def printMorphemeScore(self,morpheme):
        if self.evaluation.has_key(morpheme):
            print "「" + morpheme + "」"
            for j in self.roleList:
                print  j +":"+ str(self.evaluation[morpheme][j])
  
    def checkEvaluations(self):
        r = random.randint(0,len(self.evaluation.keys())-1)
        r2 = random.randint(0,len(self.evaluation.keys())-1)
        r3 = random.randint(0,len(self.evaluation.keys())-1)
        print self.evaluation.keys()[r]
        print self.evaluation[self.evaluation.keys()[r]]
        print self.evaluation.keys()[r2]
        print self.evaluation[self.evaluation.keys()[r2]]
        print self.evaluation.keys()[r3]
        print self.evaluation[self.evaluation.keys()[r3]]
        
    
        print "**********************"
        print "<主要なワード>"
        words = ["占い","霊能","狩人","共有","噛み","吊り","CO"]
        for w in words:
            if self.evaluation.has_key(w):
                print "【"+w+"】"
                for j in self.evaluation[w].keys():
                    print "*%s,%f" %( j , self.evaluation[w][j])

    def saveParameters(self,destfilename = PATH + "parameters/role_evaluation"):
        f = open(destfilename,"w+")
        for key in self.evaluation.keys():
            text = "%s:" % key
            for i in self.evaluation[key].values():
                text += str(i) + ","
            text = text[:-1] + "\n"
            f.write(text)
        f.close()

#ソースファイルから整型したparsed_logの作成、parsed_logからの発言データの復元。
class LogManager():
    def __init__(self):
        self.log = {} #名前をキーとしたハッシュ。同名の別キャラクターも考慮し、キャラクタデータの配列characters[]を要素とする。
                      #characters[i]はlife,role,texts を要素として持つ。それぞれ、最終的な生存・役職・喋った台詞。

    #parsed_logからキャラクタ毎の記録を生成。
    def loadParsedLog(self,srcfilename = FilePath.PATH + FilePath.PARSED_LOG):
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
    def parseWakameteLog(self,srcfilename = PATH  + "logfiles/log_src",characters = {}):
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
       
    def saveParsedLog(self,destfilename = "./log_analyzer/parsed_log",option = "a"):
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
#########実行ファイル時#############

if __name__ == "__main__":
    params = sys.argv
    argc = len(params)
    logmanager = LogManager()
    if argc <= 1 : 
        print "********************************************"
        print "引数が正しくありません"
        print "********************************************"
        exit()

    mode = params[1]
    if mode == "-parse" :
        if (argc <= 1):
            log_srcfilename = PATH + "logfiles/log_src"
            logmanager.getLog(log_srcfilename)
            log_srcfilename = PATH + "logfiles/log_src2"
            logmanager.getLog(log_srcfilename)
            log_srcfilename = PATH + "logfiles/log_src3"
            logmanager.getLog(log_srcfilename)
            parsed_logfilename = PATH + "logfiles/parsed_log"
        elif (argc == 2):
            print "error : 出力ファイル名を指定してください\n"
            exit()
        elif (argc >= 3):
            log_srcfilename = PATH + "logfiles/" + params[2]
            logmanager.getLog(log_srcfilename)
            parsed_logfilename = PATH + "logfiles/" + params[3]

        logmanager.saveParsedLog(parsed_logfilename,"w+")
    elif mode == "-learn":
        parsed_log = "parsed_log"
        if (argc >= 3):
            parsed_log = params[2]
        logmanager.loadParsedLog(PATH + "logfiles/" + parsed_log)
        inferencer = RoleInferenceEngine(logmanager)
        inferencer.learn()
        inferencer.checkEvaluations()
        inferencer.saveParameters()

    elif mode == "-infer":
        role = params[2]
        #保存したパラメータをまだ使用していない
        logmanager.loadParsedLog(FilePath.PATH + FilePath.PARSED_LOG)
        inferencer = RoleInferenceEngine(logmanager)
        inferencer.learn()
        inferencer.roleInferenceTest(role)
    else:
        print "引数が正しくありません"

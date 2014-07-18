# coding: utf-8 
import random
import MeCab
import re
import sys,os

sys.path.append(os.pardir)
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/" + os.pardir)
#print os.pardir
#print os.path.dirname(os.path.abspath(__file__))
from werewolf_dictionary import Const


#この先の予定：
#単体の形態素・マルコフ遷移だけではなく、複数行前の文のパラメータに応じて分類をする。どう分類をする？
#発言の方は難しい。発言パターンを大量に登録して、どれを使うかを選ぶ。
#ある状況のある文に対して、一番人狼っぽさが低い発言を行う、とか？

class PlayersLog():
    def __init__(self):
        self.log = {}
        self.jobList = Const.JobNameWords.values()
        self.counts = {}
        self.evaluation = {}
        self.speakNums = {}
        self.jobSuspection = {}
        for j in self.jobList:
            self.jobSuspection[j] = 0.0
            self.speakNums[j] = 0
    def pickUpJob(self,job_name):
        players_list = [] 
        for name in self.log.keys():
            for character in self.log[name]: 
                if character["job"] == job_name:
                    players_list.append(character)
        return players_list

    #わかめてのログ用のパーサ。中間ファイルを生成。
    def parseWakameteLog(self,srcfilename = "./log_analyzer/log_src.txt",characters = {}):
        f = open(srcfilename, "r")
        line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
        while line:
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
                        character_job = re.search('\[(.+)\]',line).group(1).strip().replace("　	","").replace("　","")
                        line = f.readline() #生存状況
                        character_life = re.search('（(.+)）',line).group(1).strip().replace("　	","").replace("　","")
                        idx = 0
                        if characters.has_key(character_name): 
                            characters[character_name].append({})
                            idx = len(characters[character_name]) - 1 #同名のキャラクタに備えてハッシュの配列にしておく
                        else:
                            characters[character_name] = [{}]
                        characters[character_name][idx]["job"] = character_job
                        characters[character_name][idx]["life"] = character_life
                        characters[character_name][idx]["texts"] = []
                    # characters : 名前をキーにして、職業・最終的な生存・喋った言葉　を持つハッシュ。同名の場合は配列に。
                    #プレイヤーの台詞
            m = re.match('◆([^\s]+)?さん[^の念話]+\s*(「.*)?',line) 
            if not m == None :#192.168.20.2
                name = m.group(1).strip().replace("\t","").replace("　","").replace("　","")
                text = ""
                if not m.group(2) == None:
                    text = m.group(2).replace("「","").replace("」","")
                if characters.has_key(name) and not text == "": #仮で入って途中から名前変えた場合と、二行にまたがった発言は除く
                    idx = len(characters[name]) - 1 #同名のプレイヤーは基本的に最新のものを見続ける
                    characters[name][idx]["texts"].append(text)
                    #村ごとに作る場合はこちらで。
                    #f2.write(name + "(" +characters[name][idx]["job"] + ")" + "「" + text  + "」"+ "\n") # 引数の文字列をファイルに書き込む
            line = f.readline()
        
       # player_names = characters.keys()
       # for name in player_names:
       #     for character in characters[name]: 
       #         for text in character["texts"]:
       #             f2.write(name + "(" +character["job"] + ")" + "「" + text  + "」"+ "\n") # 引数の文字列をファイルに書き込む 
        f.close()
        return characters

    def getLog(self,srcfilename = "./log_analyzer/log_src.txt"):
         self.parseWakameteLog(srcfilename,self.log)
       
    def saveParsedLog(self,destfilename = "./log_analyzer/log_dest.txt"):
        f2 = open(destfilename, "a")
        for name in self.log.keys():
            for character in self.log[name]: 
                for text in character["texts"]:
                    f2.write(name + "(" +character["job"] + ")" + "「" + text  + "」"+ "\n") # 引数の文字列をファイルに書き込む 
        f2.close()
        
    def learn(self):
        t = MeCab.Tagger("-Owakati")
        for job in Const.JobNameWords.values():
            players = self.pickUpJob(job)
            for player in players:
                for text in player["texts"]:
                    m = t.parse(text)
                    result = m.rstrip(" \n").split(" ")
                    for morpheme in result:
                        self.addMorpheme(job,morpheme) #形態素を辞書に追加
        self.morphemeScoring()

    def addMorpheme(self,job,morpheme): #
        if not self.evaluation.has_key(morpheme):
            h = {}
            h2 = {}
            for j in self.jobList:
                h[j] = 0
                h2[j] = 0.0
            self.counts[morpheme] = h
            self.evaluation[morpheme] = h2
        self.speakNums[job] += 1
        self.counts[morpheme][job] += 1
    def morphemeScoring(self):
        for morpheme in self.evaluation.keys():
            c = sum(self.counts[morpheme].values()) * 1.0
            for j in self.jobList:
                if not self.speakNums[j] == 0:
                    #全員が良く言う言葉(役職名、挨拶)は頻度が当然高くなるので補正するため他の役職の発言数でも割る
                    CONST = 4 #自分の発言数をどこまで除くべきか？除かなくていいのか？とりあえず人狼がちゃんと人狼と判定されるとこまで。
                    c2 = c - self.counts[morpheme][j]/CONST if not c == self.counts[morpheme][j] else 1.0
                    s = self.counts[morpheme][j] / c2 / self.speakNums[j]
                    self.evaluation[morpheme][j] = s
        r = random.randint(0,len(self.evaluation.keys())-1)
        r2 = random.randint(0,len(self.evaluation.keys())-1)
        r3 = random.randint(0,len(self.evaluation.keys())-1)
        #print self.evaluation.keys()[r]
        #print self.evaluation[self.evaluation.keys()[r]]
        #print self.evaluation.keys()[r2]
        #print self.evaluation[self.evaluation.keys()[r2]]
        #print self.evaluation.keys()[r3]
        #print self.evaluation[self.evaluation.keys()[r3]]
        
        
        #
        #for morpheme 
        #何を学習データにする？とりあえず各役職ごとに 
        #1. 各ワードに対して、ワードを発言した回数 / その役職の合計ワード発言回数 / 他の役職のそのワード発言回数
        #で、特定の役職のよく言っているワードを調べる。
    


    def jobDistinction(self,text):
        t = MeCab.Tagger("-Owakati")
        m = t.parse(text)
        result = m.rstrip(" \n").split(" ")
        for morpheme in result:
            if self.evaluation.has_key(morpheme):
                for j in self.jobList:
                    self.jobSuspection[j] += self.evaluation[morpheme][j] 
        max = 0
        job = None
        for j in self.jobSuspection.keys():
            if self.jobSuspection[j] >= max:
                max = self.jobSuspection[j]
                job = j
        return job
    def judgeTest(self,job = "wolf"): 
        srcfilename = "./log_analyzer/text_" + job +".txt"
        f = open(srcfilename, "r")
        line = f.readline() 
        while line:
            m = re.search('.+\(.+\)「(.+)」',line)
            if m :
                text = m.group(1)
                print self.jobDistinction(text)
            line = f.readline()
        f.close()       
        total = 0
        for tp in self.jobSuspection.items():
            total += tp[1]
        for tp in self.jobSuspection.items():
            print tp[0] + ":" + str(100 * tp[1] / total) + "%"
    def printMorphemeScore(self,morpheme):
        if self.evaluation.has_key(morpheme):
            print "「" + morpheme + "」"
            for j in self.jobList:
                print  j +":"+ str(self.evaluation[morpheme][j])
#########実行ファイル時#############

if __name__ == "__main__":
    params = sys.argv
    log = PlayersLog()
    if len(params) >= 3 :
        srcfilename = params[1]
        destfilename = params[2]
        log.getLog(srcfilename)
        log.saveParsedLog(destfilename)
    else:
        log.getLog("./log_analyzer/log_src.txt")
        log.getLog("./log_analyzer/log_src2.txt")
        log.getLog("./log_analyzer/log_src3.txt")
        #log.saveParsedLog()
        log.learn()
        log.judgeTest("lunatic")
        #log.printMorphemeScore("○")

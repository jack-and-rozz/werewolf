# coding: utf-8 
import random
import MeCab
import re
import sys,os

sys.path.append(os.pardir)
#from werewolf_dictionary import Const
#print os.pardir
#print os.path.dirname(os.path.abspath(__file__))


class PlayersLog():
    def __init__(self):
        self.dictionary = {}

    #わかめてのログ用のパーサ。中間ファイルを生成。
    def parseLog(self,srcfilename = "./log_analyzer/log_src.txt",destfilename = "./log_analyzer/log_dest.txt"):
        players_log = PlayersLog()
        f = open(srcfilename, "r")
        f2 = open(destfilename, "a")
        line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
        characters = {}
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
                        #print "%s[%s](%s)" % (character_name,character_job,character_life)
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
            line = f.readline()

        player_names = characters.keys()
        for name in player_names:
            for character in characters[name]: 
                for text in character["texts"]:
                    f2.write(name + "(" +character["job"] + ")" + "「" + text  + "」"+ "\n") # 引数の文字列をファイルに書き込む 
        f.close()
        f2.close()
        self.dictionary = characters

######実行ファイル時###########

if __name__ == "__main__":
    params = sys.argv
    players_log = PlayersLog()
    if len(params) >= 3 :
        srcfilename = params[1]
        destfilename = params[2]
        players_log.parseLog(srcfilename,destfilename)
    else:
        players_log.parseLog()
        

# coding:utf-8

"""
memo
 [x for x in [1,2,3,4,5] if x > 3]
"""
class Const:
    #定数。被らないように。
    Wolf = 0
    Lunatic = 1
    Villager = 2
    Seer = 3
    Medium = 4
    Hunter = 5
    Freemason = 6
    Fox = 7
    
    Night = 98
    Day = 99

    WinVillage = 100
    WinWolves = 101


    #ある情報の信用度について
    RULE = 1000 #全員が事実であると分かっていること。
    TRUTH = 999 #事実だと少なくとも自分は分かっていること。
    NEVER = -999 #事実ではないと少なくとも自分は分かっていること。
    #A,Bの候補。
    TotalWolves = "狼の合計"
    TotalLivingWolves = "生きている狼"
    Living = "生きている"
    Dead = "死んでいる"
    Self = "自分"
    Human = "人間"
    TotalLivingHuman = "生きている人間"



    NoOne = -99

    JobNameWords = {
        Wolf : "狼",
        Lunatic : "狂",
        Seer : "占",
        Medium : "霊",
        Hunter : "狩",
        Villager : "村",
        Freemason : "共",
        Fox : "狐"
    }
    JobsList = [Wolf,Villager,Villager,Villager,Seer,Wolf,Medium,Villager,Lunatic,Hunter,Villager,Villager,Villager,Freemason,Freemason,Villager,Villager]
    ActorNameListA = ["楽天家","村長","老人","神父","木こり","旅人","ならず者","少年","少女","行商人","羊飼い","パン屋","青年","村娘","農夫","宿屋の女主人","シスター","仕立屋","司書","負傷兵"]
    ActorNameListB = ["ゲルト","ヴァルター","モーリッツ","ジムゾン","トーマス","ニコラス","ディーター","ペーター","リーザ","アルビン","カタリナ","オットー","ヨアヒム","パメラ","ヤコブ","レジーナ","フリーデル","エルナ","クララ","シモン"]


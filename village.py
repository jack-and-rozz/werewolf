# coding:utf-8
from werewolf_dictionary import Const
from letra_util import LetraWerewolfUtil
from actor import Actor
import random
import time


"""
仕様：
1.最多得票が複数いた場合は再投票無しでランダムに選択
2.狐は今んとこなし
3.狩人は自分守れず。
4.とりあえず初日はあり。
"""

class Village: #実際のゲーム処理
    from werewolf_dictionary import Const 
    def __init__(self,actors_num):
        self.day = 0
        self.phase = Const.Night
        self.actors = self.createActors(actors_num)
        self.executed_list = [None]
        self.protected_list = [None]
        self.killed_list = [None]
        self.chatlogs = [[{"actor_id" : -1, "words" : "0日目です。ゲームが始まりました..."}]]
        self.votelogs = [{"vote_for":None,"obtained":None}] #誰が誰に投票したかとまとめた得票数が記録される
        self.chatting_time = 10
        self.wolves = []
        self.lunatic = None
        self.seer = None
        self.medium = None
        self.hunter = None
        self.freemasons = []
        self.fox = None
        self.checkActorsRoles()


    def start(self):
        self.gameInit()
        self.nightPhase()
    def gameInit(self): #Actorインスタンスが生成されてから決定する事を伝える(合計actorの人数とか)
        for actor in self.actors:
            actor.thinkInit()

    def checkActorsRoles(self): #各職業が誰か記録する
        for actor in self.actors :
            if actor.role.role_id == Const.Wolf:
                self.wolves.append(actor.role)
            elif actor.role.role_id == Const.Lunatic:
                self.lunatic = actor.role
            elif actor.role.role_id == Const.Seer:
                self.seer = actor.role
            elif actor.role.role_id == Const.Medium:
                self.medium = actor.role
            elif actor.role.role_id == Const.Hunter:
                self.hunter = actor.role
            elif actor.role.role_id == Const.Freemason:
                self.freemasons.append(actor.role)
            elif actor.role.role_id == Const.Fox:
                self.fox.append(actor.role)

    def printVotingLog(self,day):
        print ""
        vote_for = self.votelogs[day]["vote_for"]
        obtained =  self.votelogs[day]["obtained"]
        for actor in self.actors:
            if not vote_for[actor.id] == Const.NoOne:
                resultStr = actor.name +  "(" + str(obtained[actor.id]) +"票)→　" + self.actors[vote_for[actor.id]].name
                print resultStr
        print ""
        return
    def printVillageState(self):
        print "\n--- " + str(self.day) + "日目 "+ ("夜" if self.phase == Const.Night else "昼") +" ---    "  
        self.printAllActors()
        print ""
        print "(吊) : ",
        for executed in self.executed_list:
            if not executed == None:
                print executed.name,
            else : 
                print "✕",

        print ""
        print "(殺) : ",
        for killed in self.killed_list:
            if not killed == None:
                print killed.name,
            else : 
                print "✕",
        print ""
    def printAllActors(self):
        print "生存 (%d人) :" % len(self.livingActors()) ,
        for living in self.livingActors():
            print living.name + "  ",
        print ""
        print "死亡 (%d人) :" % len(self.deadActors()) ,
        for dead in self.deadActors():
            print dead.name + "  ",
        print ""

    def printAllActorsDetail(self):
        print "生存 (%d人) :" % len(self.livingActors()) ,
        for i in range(0,len(self.livingActors())):
            print self.livingActors()[i].name + "(" + Const.RoleNameWords[self.livingActors()[i].role.role_id] + ")  ",
        print ""
        print "死亡 (%d人) :" % len(self.deadActors()) ,
        for i in range(0,len(self.deadActors())):
            print self.deadActors()[i].name + "(" + Const.RoleNameWords[self.deadActors()[i].role.role_id] + ")  ",
        print ""
    def livingActors(self):
        list = []    
        for actor in self.actors:
            if actor.is_living:
                list.append(actor)
        return list
    def deadActors(self):
        list = []    
        for actor in self.actors:
            if not actor.is_living:
                list.append(actor)
        return list

    def isGameOver(self):
        white = 0
        black = 0
        for actor in self.livingActors():
            if actor.role.role_id == Const.Wolf:
                black += 1
            else:
                white += 1
        if white <= black:
            return Const.WinWolves
        elif black == 0: 
            return Const.WinVillage
        else:
            return 0
        
    def votingPhase(self):
        vote_for = []
        obtained = []
        for i in range(len(self.actors)):
            obtained.append(0)
            vote_for.append(-1)
        for actor in self.livingActors():
            voted_actor_id = actor.vote()
            obtained[voted_actor_id] += 1 
            vote_for[actor.id] = voted_actor_id 
        self.votelogs.append({"obtained": obtained,"vote_for" : vote_for}) #誰が誰に投票したかと獲得総投票数を保存

        executed_id_list =  [i for i,j in enumerate(obtained) if j == max(obtained)]
        random.shuffle(executed_id_list)  #最多票が複数あった場合ランダムに選択
        actor = self.actors[executed_id_list[0]]
        self.execute(actor)
        self.printVotingLog(self.day)
        print "<System> : 投票の結果、" + actor.name + "さんが処刑されました。"
        return actor
    def execute(self,actor):
        actor.is_living = False
        self.executed_list.append(actor)
        return actor
    def chattingPhase(self):
        #とりあえずランダムに誰か選んで喋らせる。
        i = 0
        time.sleep(0.8)
        while i < self.chatting_time:
            i+=1
            r = random.randint(0,len(self.livingActors())-1)
            actor = self.livingActors()[r]
            actor.speak()
            for other in self.livingActors():
                if not other.id == actor.id:
                    actor.hear()
            time.sleep(0.05)
        return 
    def addToChatlogs(self,actor_id,words):
        self.chatlogs[self.day].append({"actor_id":actor_id,"words":words})
    def toNextDay(self):
        self.day += 1
        self.chatlogs.append([])
    def dayPhase(self):
        self.toNextDay()
        self.phase = Const.Day
        self.printVillageState()
        print ""
        if self.killed_list[self.day] == None:
            print "<System> : 昨日の夜は誰も殺されていませんでした。"
        else:
            print "<System> : " + self.killed_list[self.day].name + "さんが無残な姿で発見されました。"

        self.chattingPhase()
        self.votingPhase()

        if self.isGameOver() == Const.WinVillage:
            print "\n<System> : 全ての人狼を退治した……。人狼に怯える日々は去ったのだ！"
            self.endGame();
        elif self.isGameOver() == Const.WinWolves:
            print "\n<System> : もう人狼に対抗できるほど村人は残っていない・・・人狼は全ての村人を食い、次の村へと去っていった。"
            self.endGame();
   
        else:
            self.nightPhase()
        return 
    def nightPhase(self):
        self.phase = Const.Night
        self.printVillageState()

        self.seer.inspection()
        self.medium.mediumTelling()
        self.hunter.protection()
        self.leaderWolf().attack()
        if self.isGameOver() == Const.WinVillage:
            print "\n<System> : 全ての人狼を退治した……。人狼に怯える日々は去ったのだ！"
            self.endGame();
        elif self.isGameOver() == Const.WinWolves:
            print "\n<System> : もう人狼に対抗できるほど村人は残っていない・・・人狼は全ての村人を食い、次の村へと去っていった。"
            self.endGame();
        else:
            self.dayPhase()
        return

    def leaderWolf(self):
        for wolf in self.wolves : #生きている人狼のうち先頭のものを選ぶ
            if self.actors[wolf.actor_id].is_living:
                return wolf
    def endGame(self):
        print ""
        self.printAllActorsDetail()
    def createActors(self,actors_num):
        actors = []
        r = random.randint(0,len(Const.ActorNameListA)-actors_num)
        name_nums_list = range(0+r,actors_num+r)
        role_nums_list = range(0,actors_num)
        random.shuffle(name_nums_list)
        random.shuffle(role_nums_list)
        for i in range(0,actors_num):
            id = i
            role_id = Const.RolesList[role_nums_list[i]] 
            name = LetraWerewolfUtil.makeDefaultName(name_nums_list[i])
            village = self
            actors.append(Actor(i,name,role_id,village))
        return actors    

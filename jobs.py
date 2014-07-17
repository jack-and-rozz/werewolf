# coding:utf-8
from werewolf_dictionary import Const
import random

class Job:
    def __init__(self,actor_id,village):
        self.village = village
        self.actor_id = actor_id
        self.name = Const.JobNameWords[self.job_id]
    def isWolf(self):
        return False

class Villager(Job):
    def __init__(self,actor_id,village):
        self.job_id =  Const.Villager
        Job.__init__(self,actor_id,village)


class Wolf(Job):
    def __init__(self,actor_id,village):
        self.job_id =  Const.Wolf
        Job.__init__(self,actor_id,village)
    def isWolf(self):
        return True
    def attack(self):
        actor = self.decideAttackTarget()
        if self.village.protected_list[-1] == actor or actor.job.job_id == Const.Fox:
            self.village.killed_list.append(None)
            return False
        else:
            actor.is_living = False
            self.village.killed_list.append(actor)
            return True 
    def decideAttackTarget(self):
        living = self.village.livingActors()
        for actor in living:
            if actor.job.isWolf():
                living.remove(actor)
        i = random.randint(0,len(living)-1)
        victim = living[i]
        return victim

class Lunatic(Job):
    def __init__(self,actor_id,village):
        self.job_id =  Const.Lunatic
        Job.__init__(self,actor_id,village)

class Seer(Job):
    def __init__(self,actor_id,village):
        self.job_id =  Const.Seer
        self.inspection_list = []
        Job.__init__(self,actor_id,village)
    def inspection(self):
        actor = self.decideInspectTarget()
        if actor.job.isWolf():
            return True
        else:
            return False
    def decideInspectTarget(self):
        inspections = self.village.livingActors()
        for actor in inspections:
            if actor.id == self.actor_id:
                inspections.remove(actor)
                i = random.randint(0,len(inspections)-1)
                actor =  inspections[i]
        return actor
        

class Medium(Job):
    def __init__(self,actor_id,village):
        self.job_id =  Const.Medium
        self.medium_telling_list = []
        Job.__init__(self,actor_id,village)
    def mediumTelling(self):
        if self.village.executed_list[-1] == None :
            self.medium_telling_list.append(None)
        elif self.village.executed_list[-1].job.job_id == Const.Wolf:
            self.medium_telling_list.append(True)
        else:
            self.medium_telling_list.append(False)
     
class Hunter(Job):
    def __init__(self,actor_id,village):
        self.job_id =  Const.Hunter
        Job.__init__(self,actor_id,village)
    def protection(self):
        actor = self.decideProtectTarget()
        self.village.protected_list.append(actor)
        return

    def decideProtectTarget(self):
        if self.village.actors[self.actor_id].is_living:
            protections = self.village.livingActors()
            for actor in protections:
                if actor.id == self.actor_id:
                    protections.remove(actor)
                    i = random.randint(0,len(protections)-1)
                    actor = protections[i]
            return actor
        else:
            return None

class Freemason(Job):
    def __init__(self,actor_id,village):
        self.job_id =  Const.Freemason
        Job.__init__(self,actor_id,village)

class Fox(Job):
    def __init__(self,actor_id,village):
        self.job_id =  Const.Fox
        Job.__init__(self,actor_id,village)





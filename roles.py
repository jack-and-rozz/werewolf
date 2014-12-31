# coding:utf-8
from utils import Const
import random

class Role:
    def __init__(self,actor_id,village):
        self.village = village
        self.actor_id = actor_id
        self.name = Const.RoleNameWords[self.role_id]
    def isWolf(self):
        return False

class Villager(Role):
    def __init__(self,actor_id,village):
        self.role_id =  Const.Villager
        Role.__init__(self,actor_id,village)


class Wolf(Role):
    def __init__(self,actor_id,village):
        self.role_id =  Const.Wolf
        Role.__init__(self,actor_id,village)
    def isWolf(self):
        return True
    def attack(self):
        actor = self.decideAttackTarget()
        if self.village.protected_list[-1] == actor or actor.role.role_id == Const.Fox:
            self.village.killed_list.append(None)
            return False
        else:
            actor.is_living = False
            self.village.killed_list.append(actor)
            return True 
    def decideAttackTarget(self):
        living = self.village.livingActors()
        for actor in living:
            if actor.role.isWolf():
                living.remove(actor)
        i = random.randint(0,len(living)-1)
        victim = living[i]
        return victim

class Lunatic(Role):
    def __init__(self,actor_id,village):
        self.role_id =  Const.Lunatic
        Role.__init__(self,actor_id,village)

class Seer(Role):
    def __init__(self,actor_id,village):
        self.role_id =  Const.Seer
        self.inspection_list = []
        Role.__init__(self,actor_id,village)
    def inspection(self):
        actor = self.decideInspectTarget()
        if actor.role.isWolf():
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
        

class Medium(Role):
    def __init__(self,actor_id,village):
        self.role_id =  Const.Medium
        self.medium_telling_list = []
        Role.__init__(self,actor_id,village)
    def mediumTelling(self):
        if self.village.executed_list[-1] == None :
            self.medium_telling_list.append(None)
        elif self.village.executed_list[-1].role.role_id == Const.Wolf:
            self.medium_telling_list.append(True)
        else:
            self.medium_telling_list.append(False)
     
class Hunter(Role):
    def __init__(self,actor_id,village):
        self.role_id =  Const.Hunter
        Role.__init__(self,actor_id,village)
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

class Freemason(Role):
    def __init__(self,actor_id,village):
        self.role_id =  Const.Freemason
        Role.__init__(self,actor_id,village)

class Fox(Role):
    def __init__(self,actor_id,village):
        self.role_id =  Const.Fox
        Role.__init__(self,actor_id,village)





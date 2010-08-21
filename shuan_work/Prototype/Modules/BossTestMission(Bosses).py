#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission root module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from Enemies import Boss1, Boss2
from Effects import BossMessage

from .Core.MissionTemplate import MissionTemplate

class Mission(MissionTemplate):
    '''
    Shuan gameplay slice prototype mission root class
    '''
    name = 'Simple Mission'
    speed = 1
    landTexture = 'mars'
    
    boss = None
    bossMeter = None
    
    bossesList = [Boss1.Enemy, Boss2.Enemy]
    bossTimer = 5000
    
    def __init__(self):
        MissionTemplate.__init__(self)
        self.startTimer = self.startTime
    
    def update(self):
        '''
        Level update
        '''
        t = self.getTimer()
        
        if t >= self.startTimer + self.bossTimer and self.boss == None:
            self.boss = self.bossesList.pop(0)()
            self.bossMeter = BossMessage.BossMessage(self.context)
        
        #If you are going to rewrite the update method, fon's forget to add this call in the end.
        self.finishUpdate()
    
    def objectives(self):
        if self.boss is None:
            return False
        
        if self.boss.life <= 0 and len(self.bosses) == 0:
            self.bossMeter.kill()
            return True
        elif self.boss.life <= 0:
            self.bossMeter.kill()
            self.startTimer = self.getTimer()
            self.boss = None
            return True
        else:
            return False
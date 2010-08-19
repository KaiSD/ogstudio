#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission root module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from Enemies import Enemy1, Enemy2, Enemy3, Boss1
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
    
    def update(self):
        '''
        Level update
        '''
        t = self.getTimer()
                
        if t < 110000:
            self.randomSpawner(30 + 40000 / t, Enemy3.Enemy,
                               Enemy2.Enemy, Enemy2.Enemy, 
                               Enemy2.Enemy, Enemy1.Enemy, 
                               Enemy2.Enemy, Enemy1.Enemy,
                               Enemy2.Enemy, Enemy1.Enemy)
        elif t < 120000:
            self.randomSpawner(30 + t / 500, Enemy3.Enemy, Enemy2.Enemy, Enemy1.Enemy)
        elif t > 120000 and self.boss is None:
            self.boss = Boss1.Enemy()
            self.bossMeter = BossMessage.BossMessage(self.context)
        
        #If you are going to rewrite the update method, fon's forget to add this call in the end.
        self.finishUpdate()
    
    def objectives(self):
        if self.getTimer() > 120000: 
            if self.boss.life <= 0:
                self.bossMeter.kill()
                return True
            else:
                return False
        else:
            return False
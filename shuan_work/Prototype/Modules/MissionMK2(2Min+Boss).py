#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission root module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from Enemies import Enemy1, Enemy2, Enemy22, Enemy3, Boss2
from Effects import BossMessage

from .Core.MissionTemplate import MissionTemplate

class Mission(MissionTemplate):
    '''
    Shuan gameplay slice prototype mission root class
    '''
    name = 'Simple Mission'
    speed = 2
    landTexture = 'mars'
    
    boss = None
    bossMeter = None
    
    def update(self):
        '''
        Level update
        '''
        t = self.getTimer()

        if t < 115000:
            self.randomSpawner(40 + 40000 / t,
                               Enemy2.Enemy, Enemy22.Enemy, 
                               Enemy2.Enemy, Enemy1.Enemy, 
                               Enemy2.Enemy, Enemy1.Enemy,
                               Enemy2.Enemy, Enemy1.Enemy)
        elif t < 120000:
            self.randomSpawner(40 + t / 500, Enemy22.Enemy, Enemy2.Enemy, Enemy1.Enemy)
        elif t > 120000 and self.boss is None:
            self.boss = Boss2.Enemy()
            self.bossMeter = BossMessage.BossMessage(self.context)
        
        #If you are going to rewrite the update method, fon's forget to add this call in the end.
        self.finishUpdate()
    
    def objectives(self):
        if self.getTimer() > 120000 and not self.boss is None: 
            if self.boss.life <= 0:
                self.bossMeter.kill()
                return True
            else:
                return False
        else:
            return False
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default enemy module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EnemyTemplate import EnemyTemplate

from ..EnemyWeapons.EnemyLaser import Weapon as Gun 

class Enemy(EnemyTemplate):
    '''
    Standart Enemy
    '''
    images = EnemyTemplate.context.loadSprite('enemy22.png', [(0, 0, 33, 34)])

    # Mechanics params
    speed = 3
    attackTreashold = 10000
    attackTreasholdStart = 70
    attackTreasholdEnd = 50
    firing2 = False
    life = 475
    weapon2 = Gun(16, 19)
    damage = 100
    
    xMove = True
    xMoveChange = True
    
    def update(self):
        EnemyTemplate.update(self)
        
        if self.isDo(self.attackTreasholdStart) and not self.context.currentLevel.finished:
            self.firing2 = True
        
        if self.firing2:
            self.weapon2.fire(self.rect)
            if not self.weapon2.soundEnd is None:
                self.weapon2.soundEnd.set_volume(0.5)
                self.weapon2.soundEnd.play()
            if self.isDo(self.attackTreasholdEnd) or self.context.currentLevel.finished:
                self.firing2 = False
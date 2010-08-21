#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default enemy module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EnemyTemplate import EnemyTemplate

from ..EnemyWeapons.EnemyLaser import Weapon as Gun2
from ..EnemyWeapons.EnemyAimGun import Weapon as Gun1  

class Enemy(EnemyTemplate):
    '''
    Standart Enemy
    '''
    images = EnemyTemplate.context.loadSprite('boss.png', [(0, 0, 107, 86)])

    # Mechanics params
    speed = 2
    attackTreashold = 20
    attackTreasholdStart = 20
    attackTreasholdEnd = 40
    firing2 = False
    life = 16000
    weapons = [Gun1(26, 79), Gun1(80, 79)]
    weapon2 = Gun2(53, 86)
    damage = 100
    weaponTicks = 0
    
    xMove = True
    xMoveChange = True
    
    yMove = True
    yMoveStay = True
    
    isEvil = True
    
    def update(self):
        EnemyTemplate.update(self)
        
        if self.isDo(self.attackTreasholdStart) and not self.context.currentLevel.finished:
            self.firing2 = True
        
        if self.firing2:
            self.weapon2.fire(self.rect, self.weaponTicks)
            self.weaponTicks += 1
            if not self.weapon2.soundEnd is None:
                self.weapon2.soundEnd.set_volume(0.5)
                self.weapon2.soundEnd.play()
            if self.isDo(self.attackTreasholdEnd) or self.context.currentLevel.finished:
                self.firing2 = False
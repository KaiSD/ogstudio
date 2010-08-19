#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default enemy module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EnemyTemplate import EnemyTemplate

from ..EnemyWeapons.EnemyAimGun import Weapon as Gun2
from ..EnemyWeapons.EnemyGun import Weapon as Gun1  

class Enemy(EnemyTemplate):
    '''
    Standart Enemy
    '''
    images = EnemyTemplate.context.loadSprite('boss.png', [(0, 0, 107, 86)])

    # Mechanics params
    speed = 2
    attackTreashold = 30
    attackTreashold2 = 30
    life = 12000
    weapons = [Gun1(26, 79), Gun1(80, 79)]
    weapon2 = Gun2(53, 86)
    damage = 100
    
    xMove = True
    xMoveChange = True
    
    yMove = True
    yMoveStay = True
    
    isEvil = True
    
    def update(self):
        EnemyTemplate.update(self)
        
        if self.isDo(self.attackTreashold2):
            self.weapon2.fire(self.rect)
            if not self.weapon2.soundEnd is None:
                self.weapon2.soundEnd.set_volume(0.5)
                self.weapon2.soundEnd.play()
        
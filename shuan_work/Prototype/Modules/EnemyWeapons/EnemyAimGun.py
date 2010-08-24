#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.EnemyAimingBullet import Bullet

class Weapon(WeaponTemplate):
    '''
    Enemy gun
    '''
    reloadTime = 0
    damage = 15
    soundEnd = WeaponTemplate.context.loadSound('enemy_shot.wav')

    def __init__(self, posX, posY):
        '''
        Constructor
        '''
        self.reloadTimer = 0
        self.justFired = 0
        
        self.posX = posX
        self.posY = posY
        
        if not 'EnemyAimGun' in self.context.debug.keys():  
            self.context.debug['EnemyAimGun'] = 0 
    
    def fire(self, rect, counter=0):
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage)
        self.context.debug['EnemyAimGun'] += 1
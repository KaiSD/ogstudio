#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.EnemyBullet import Bullet

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
    
    def fire(self, rect, counter=0):
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage)
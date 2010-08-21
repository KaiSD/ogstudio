#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.MiniBullet import Bullet

class Weapon(WeaponTemplate):
    '''
    Additional very light gun
    '''
    reloadTime = 4
    damage = 10
    soundLoop = WeaponTemplate.context.loadSound('minigun_loop.wav')
    soundEnd = WeaponTemplate.context.loadSound('minigun_end.wav')
    energyCost = 15
    
    def fire(self, rect, counter):
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 0)
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.Bullet import Bullet

class Weapon(WeaponTemplate):
    '''
    Default minigun
    '''
    reloadTime = 5
    damage = 15
    soundLoop = WeaponTemplate.context.loadSound('minigun_loop.wav')
    soundEnd = WeaponTemplate.context.loadSound('minigun_end.wav')
    energyCost = 10
    
    def fire(self, rect):
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 0)
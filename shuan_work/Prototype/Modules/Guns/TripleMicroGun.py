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
    Pack of two MicroGuns. One shoots forward, one - to side.
    '''
    reloadTime = 4
    damage = 10
    soundLoop = WeaponTemplate.context.loadSound('minigun_loop.wav')
    soundEnd = WeaponTemplate.context.loadSound('minigun_end.wav')
    energyCost = 40
    
    def fire(self, rect, counter):
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 0)
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, self.side*3, 1)
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, self.side*16, 0)
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
    Minigun with less reloadTime and greater damage
    '''
    reloadTime = 4
    damage = 20
    soundLoop = WeaponTemplate.context.loadSound('minigun2_loop.wav')
    soundEnd = WeaponTemplate.context.loadSound('minigun2_end.wav')
    
    def fire(self, rect):
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 0)
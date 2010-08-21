#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.Wave import Bullet

class Weapon(WeaponTemplate):
    '''
    Plasma gun
    '''
    reloadTime = 15
    damage = 150
    soundEnd = WeaponTemplate.context.loadSound('energy.wav')
    energyCost = 60
    
    def fire(self, rect, counter):
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 0)
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.Plasma import Bullet

class Weapon(WeaponTemplate):
    '''
    Plasma gun
    '''
    reloadTime = 20
    damage = 250
    soundEnd = WeaponTemplate.context.loadSound('plasma.wav')
    
    def fire(self, rect):
        Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 0)
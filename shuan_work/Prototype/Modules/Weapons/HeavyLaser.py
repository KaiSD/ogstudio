#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.PurpleRay import Ray

class Weapon(WeaponTemplate):
    '''
    Ray gun
    '''
    reloadTime = 0
    maxReloadTime = 6
    soundLoop = WeaponTemplate.context.loadSound('laser_loop.wav')
    soundEnd = WeaponTemplate.context.loadSound('laser_end.wav')
    damage = 4
    energyCost = 36
    
    def fire(self, rect, counter=0):
        Ray((rect.left + self.posX, rect.top + self.posY), self.damage, counter)

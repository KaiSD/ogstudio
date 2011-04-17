#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.HeavyMissile import Bullet

class Weapon(WeaponTemplate):
    '''
    Self repair weapon
    '''
    damage = 60
    ammo = 1
    reloadTime = 60
    
    def __init__(self):
        WeaponTemplate.__init__(self, self.context.avatar.heavySlot[0], self.context.avatar.heavySlot[0])
    
    def fire(self, rect, counter=0):
        if self.ammo > 0:
            self.aim()
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 0, 1, self.target)
            self.ammo -= 1
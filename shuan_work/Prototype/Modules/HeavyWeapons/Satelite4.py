#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.Satelite4 import Bullet

class Weapon(WeaponTemplate):
    '''
    Self repair weapon
    '''
    damage = 120
    ammo = 3
    
    def __init__(self):
        WeaponTemplate.__init__(self, self.context.avatar.heavySlot[0], self.context.avatar.heavySlot[0])
    
    def fire(self, rect, counter=0):
        if self.ammo > 0:
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 0)
            self.ammo -= 1
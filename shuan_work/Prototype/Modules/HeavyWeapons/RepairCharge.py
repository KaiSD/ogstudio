#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate

class Weapon(WeaponTemplate):
    '''
    Self repair weapon
    '''
    damage = 30
    ammo = 3
    
    def __init__(self):
        WeaponTemplate.__init__(self, self.context.avatar.heavySlot[0], self.context.avatar.heavySlot[0])
    
    def fire(self, rect, counter=0):
        if self.ammo > 0:
            if self.context.avatar.life < self.context.avatar.baseLife:
                self.context.avatar.life += self.damage
                if self.context.avatar.life > self.context.avatar.baseLife:
                    self.context.avatar.life = self.context.avatar.baseLife
            self.ammo -= 1
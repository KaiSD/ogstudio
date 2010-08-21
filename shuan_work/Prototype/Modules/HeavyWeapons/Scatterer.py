#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.GhostBullet import Bullet

class Weapon(WeaponTemplate):
    '''
    Cheatgun fires a lots of powerfull bullets with each shot
    '''
    damage = 100
    ammo = 4
    
    def __init__(self):
        WeaponTemplate.__init__(self, self.context.avatar.heavySlot[0], self.context.avatar.heavySlot[0])
    
    def fire(self, rect, counter=0):
        if self.ammo > 0:
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, -9)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, -7)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, -5)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, -3)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, -1)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 0)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 1)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 3)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 5)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 7)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 9)
            self.ammo -= 1
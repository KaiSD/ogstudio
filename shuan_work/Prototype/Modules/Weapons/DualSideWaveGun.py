#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.SideWave import Bullet

class Weapon(WeaponTemplate):
    '''
    SideWaveGun is a small amd less powerfull model of WaveGun, shooting to sides.
    '''
    reloadTime = 6
    damage = 40
    #soundLoop = WeaponTemplate.context.loadSound('minigun_loop.wav')
    #soundEnd = WeaponTemplate.context.loadSound('minigun_end.wav')
    energyCost = 38
    
    def fire(self, rect, counter):
        if self.side > 0:
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 14, 1, None, 2.369)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 14, -1, None, 3.948)
        elif self.side < 0:
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, -14, 1, None, 0.79)
            Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, -14, -1, None, -0.79)
        else:
            if counter % 2 == 1:
                Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 14, 1, None, 2.369)
                Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, 14, -1, None, 3.948)
                self.tick = False
            else:
                Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, -14, 1, None, 0.79)
                Bullet((rect.left + self.posX, rect.top + self.posY), self.damage, -14, -1, None, -0.79)
                self.tick = True
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.SideWaveL import Bullet as BulletL
from ..Bullets.SideWaveR import Bullet as BulletR

class Weapon(WeaponTemplate):
    '''
    SideWaveGun is a small amd less powerfull model of WaveGun, shooting to sides.
    '''
    reloadTime = 6
    damage = 40
    #soundLoop = WeaponTemplate.context.loadSound('minigun_loop.wav')
    #soundEnd = WeaponTemplate.context.loadSound('minigun_end.wav')
    energyCost = 40
    
    def fire(self, rect, counter):
        if self.side > 0:
            BulletR((rect.left + self.posX, rect.top + self.posY), self.damage, 22, 0)
        elif self.side < 0:
            BulletL((rect.left + self.posX, rect.top + self.posY), self.damage, -22, 0)
        else:
            if counter % 2 == 1:
                BulletR((rect.left + self.posX, rect.top + self.posY), self.damage, 22, 0)
                self.tick = False
            else:
                BulletL((rect.left + self.posX, rect.top + self.posY), self.damage, -22, 0)
                self.tick = True
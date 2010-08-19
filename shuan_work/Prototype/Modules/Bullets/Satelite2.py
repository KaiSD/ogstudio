#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.BulletTemplate import BulletTemplate
import MiniBullet 

class Bullet(BulletTemplate):
    '''
    Explosion visual effect
    '''
    images = BulletTemplate.context.loadSprite('satelite.png', [(0, 0, 13, 13)])
    speed = 1
    shootSpeed = 4
    shootTimer = 0
    
    shotDamage = 50
    
    def update(self):
        if self.shootTimer <= 0: 
            MiniBullet.Bullet((self.rect.centerx, self.rect.centery), self.shotDamage, 16, 0)
            MiniBullet.Bullet((self.rect.centerx, self.rect.centery), self.shotDamage, -16, 0)
            self.shootTimer = self.shootSpeed
        else:
            self.shootTimer -= 1
        BulletTemplate.update(self)
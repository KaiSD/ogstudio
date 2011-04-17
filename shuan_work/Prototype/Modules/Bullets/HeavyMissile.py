#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.BulletTemplate import BulletTemplate
from ..Effects import BigDamagingExplosion 

class Bullet(BulletTemplate):
    '''
    Explosion visual effect
    '''
    images = BulletTemplate.context.loadSprite('bullets.png', [(68, 0, 8, 32)])
    speed = -5
    reAiming = True
    isRotating = True
    isSwitchTarget = True
    isAccelerating = True
    maxSpeed = 5
    explosionEffect = BigDamagingExplosion.Explosion
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.BulletTemplate import BulletTemplate

class Bullet(BulletTemplate):
    '''
    Explosion visual effect
    '''
    images = BulletTemplate.context.loadSprite('bullets.png', [(21, 1, 11, 11)])
    speed = 16
    reAiming = True
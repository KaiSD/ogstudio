#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EnemyBulletTemplate import EnemyBulletTemplate 

class Bullet(EnemyBulletTemplate):
    '''
    Explosion visual effect
    '''
    images = EnemyBulletTemplate.context.loadSprite('bullets.png',[(8, 0, 13, 13)])
    speed = 12
    aiming = False
    
    debugName = 'EnemyBullet'
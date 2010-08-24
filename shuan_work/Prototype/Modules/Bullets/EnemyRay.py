#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EnemyRayTemplate import EnemyRayTemplate

class Ray(EnemyRayTemplate):
    '''
    Explosion visual effect
    '''
    images = EnemyRayTemplate.context.loadSprite('bullets.png', [(32, 29, 9, 1),(32, 30, 9, 1),(32, 31, 9, 1)])
    
    debugName = 'EnemyRay'
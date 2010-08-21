#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.RayTemplate import RayTemplate

class Ray(RayTemplate):
    '''
    Explosion visual effect
    '''
    images = RayTemplate.context.loadSprite('bullets.png', [(32, 29, 9, 1),(32, 30, 9, 1),(32, 31, 9, 1)])
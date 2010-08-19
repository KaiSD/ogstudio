#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype explosion effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EffectTemplate import EffectTemplate 

class Explosion(EffectTemplate):
    '''
    Explosion visual effect
    '''
    images = EffectTemplate.context.loadSprite('miniExplosion.png', [(1, 1, 32, 32),
                                                                     (34, 1, 32, 32),
                                                                     (67, 1, 32, 32),
                                                                     (100, 1, 32, 32),
                                                                     (133, 1, 32, 32),                                           
                                                                     (166, 1, 32, 32)])
    sound = EffectTemplate.context.loadSound('explosion.wav')
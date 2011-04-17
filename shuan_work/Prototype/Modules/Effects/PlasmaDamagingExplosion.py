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
    images = EffectTemplate.context.loadSprite('PlasmaExplosion.png', [(1, 1, 65, 65),                                                          
                                                                    (67, 1, 65, 65),
                                                                    (133, 1, 65, 65),
                                                                    (199, 1, 65, 65),
                                                                    (265, 1, 65, 65),
                                                                    (331, 1, 65, 65),
                                                                    (397, 1, 65, 65)])
    sound = EffectTemplate.context.loadSound('explosion.wav')
    scale = 2
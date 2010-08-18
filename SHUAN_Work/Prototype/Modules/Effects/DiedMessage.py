#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype explosion effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EffectTemplate import EffectTemplate

class DiedMessage(EffectTemplate):
    '''
    Explosion visual effect
    '''
    animcycle = 8
    loop = True
    uiEffect = True
    
    def __init__(self, pos):
        self.images = [self.context.loadText('arial', 50,'Rest in peaces!', (255, 50, 50)),  self.context.loadText('arial', 50,'Rest in peaces!', (220, 0, 0))]
        EffectTemplate.__init__(self, pos)
    
    
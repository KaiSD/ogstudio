#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype explosion effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EffectTemplate import EffectTemplate

class WinMessage(EffectTemplate):
    '''
    Explosion visual effect
    '''
    animcycle = 8
    loop = True
    uiEffect = True
    
    def __init__(self, pos):
        self.images = [self.context.loadText('arial', 50, 'Mission is completed!', (220, 220, 220))]
        EffectTemplate.__init__(self, pos)
    
    
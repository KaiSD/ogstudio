#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype explosion effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EffectTemplate import EffectTemplate

class BossMessage(EffectTemplate):
    '''
    Score text visual effect
    '''
    animcycle = 8
    loop = True
    uiEffect = True
    
    def __init__(self, pos):
        self.images = [self.context.loadText('arial', 20, 'Enemy health: '+str(self.context.currentLevel.boss.life), (200, 0, 0))]
        EffectTemplate.__init__(self, pos)
        self.rect.top = pos.rect.top
    
    def update(self):
        self.images = [self.context.loadText('arial', 20, 'Enemy health: '+str(self.context.currentLevel.boss.life), (200, 0, 0))]
        EffectTemplate.update(self)
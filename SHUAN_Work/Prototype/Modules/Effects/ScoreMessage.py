#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype explosion effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EffectTemplate import EffectTemplate

class ScoreMessage(EffectTemplate):
    '''
    Score text visual effect
    '''
    animcycle = 8
    loop = True
    uiEffect = True
    
    def __init__(self, pos):
        self.images = [self.context.loadText('arial', 20, 'Score '+str(self.context.currentLevel.score), (0, 0, 200))]
        EffectTemplate.__init__(self, pos)
        self.rect.topleft = pos.rect.topleft
    
    def update(self):
        self.images = [self.context.loadText('arial', 20, 'Score '+str(self.context.currentLevel.score), (0, 0, 200))]
        EffectTemplate.update(self)
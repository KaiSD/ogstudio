#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype explosion effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EffectTemplate import EffectTemplate

class HealthMessage(EffectTemplate):
    '''
    Explosion visual effect
    '''
    animcycle = 8
    loop = True
    uiEffect = True
    
    def __init__(self, pos):
        addlife = self.context.avatar.shields
        life = self.context.avatar.life
        self.images = [self.context.loadText('arial', 20, u'Броня ' + str(life) + ' +' + str(addlife), (0, 200, 0))]
        EffectTemplate.__init__(self, pos)
        self.rect.topleft = pos.rect.topleft
        self.rect.top += 30
    
    def update(self):
        addlife = self.context.avatar.shields
        life = self.context.avatar.life
        self.images = [self.context.loadText('arial', 20, u'Броня ' + str(life) + ' +' + str(addlife), (0, 200, 0))]
        EffectTemplate.update(self)
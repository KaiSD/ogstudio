#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype explosion effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EffectTemplate import EffectTemplate

class ReactorMessage(EffectTemplate):
    '''
    Explosion visual effect
    '''
    animcycle = 8
    loop = True
    uiEffect = True
    
    def __init__(self, pos, mod):
        self.text = u'Энергия: ' + str(self.context.avatar.reactor) + '/' + str(int(100 * self.context.avatar.reactorMod)) 
        self.images = [self.context.loadText('arial', 20, self.text, (200, 200/mod, 0))]
        if mod > 1:
            self.images.append(self.context.loadText('arial', 20, self.text, (240, 240/mod, 0)))
        
        EffectTemplate.__init__(self, pos)
        self.rect.topleft = pos.rect.topleft
        self.rect.top += 90
    
    def update(self):
        EffectTemplate.update(self)
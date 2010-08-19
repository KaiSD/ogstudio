#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype explosion effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame

from ..Core import Context

class EffectTemplate(pygame.sprite.Sprite):
    '''
    Explosion visual effect
    '''
    context = Context.contextObject
    images = None
    sound = None
    
    animcycle = 4
    loop = False
    
    uiEffect = False
    
    def __init__(self, pos):
        '''
        Constructor
        '''
        if self.uiEffect:
            self.containers = self.context.ui
        else:
            self.containers = self.context.all
        
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = self.images[0]
        self.counter = 0
        self.maxcount = len(self.images)*self.animcycle
        self.rect = self.image.get_rect()
        self.rect.center = pos.rect.center
        
        if not self.sound is None:
            self.sound.play()
    
    def update(self):
        '''
        Update
        '''
        if self.loop:
            self.counter = (self.counter + 1) % self.maxcount
            self.image = self.images[self.counter/self.animcycle]
        else:
            self.image = self.images[self.counter/self.animcycle]
            self.counter = self.counter + 1
            if self.counter == self.maxcount:
                self.kill()
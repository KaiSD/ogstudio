#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame

from ..Core import Context

class BulletTemplate(pygame.sprite.Sprite):
    '''
    Explosion visual effect
    '''
    context = Context.contextObject
    images = None
    containers = context.shots, context.all
    
    animcycle = 4
    speed = 1
    ghost = False
    
    def __init__(self, pos, damage, offset=0, speedMod=1):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.counter = 0
        self.maxcount = len(self.images)*self.animcycle
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.offset = offset
        self.damage = damage
        self.speedMod = speedMod
    
    def update(self):
        '''
        Update
        '''
        self.rect.move_ip(self.offset, -self.speed*self.speedMod)
        self.counter = (self.counter + 1) % self.maxcount
        self.image = self.images[self.counter/self.animcycle]
        if self.rect.top < 0:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > self.context.rect.width:
            self.kill()
        if self.rect.bottom > self.context.rect.height:
            self.kill()
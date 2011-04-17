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
    scale = 1
    
    animcycle = 4
    loop = False
    
    uiEffect = False
    explosionEffect = None
    
    def __init__(self, pos, damage=0):
        '''
        Constructor
        '''
        if self.uiEffect:
            self.containers = self.context.ui
        elif damage > 0:
            self.containers = self.context.shots, self.context.all
            self.isExplode = False
            self.isAE = False
            self.damage = damage
            self.ghost = True
            if not self.context.debug.has_key('WeaponDamage['+str(self.__class__)+']'):
                self.context.debug['WeaponDamage['+str(self.__class__)+']'] = 0
        else:
            self.containers = self.context.all
        
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        image = self.images[0]
        if self.scale == 1:
            self.image = image
        else:
            newSize = (image.get_width()*self.scale,image.get_height()*self.scale)
            self.image = pygame.transform.smoothscale(image, newSize)
            
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
            image = self.images[self.counter/self.animcycle]
            if self.scale == 1:
                self.image = image
            else:
                newSize = (image.get_width()*self.scale,image.get_height()*self.scale)
                self.image = pygame.transform.smoothscale(image, newSize)
        else:
            image = self.images[self.counter/self.animcycle]
            if self.scale == 1:
                self.image = image
            else:
                newSize = (image.get_width()*self.scale,image.get_height()*self.scale)
                self.image = pygame.transform.smoothscale(image, newSize)
            self.counter = self.counter + 1
            if self.counter == self.maxcount:
                self.kill()
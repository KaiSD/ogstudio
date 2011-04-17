#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame, math

from ..Core import Context

class EnemyBulletTemplate(pygame.sprite.Sprite):
    '''
    Explosion visual effect
    '''
    context = Context.contextObject
    images = None
    containers = context.bombs, context.obstacles, context.all
    
    animcycle = 4
    speed = 12
    
    aiming = True
    
    isEvil = False
    
    def __init__(self, pos, damage):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.counter = 0
        self.maxcount = len(self.images)*self.animcycle
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.setfp()
        if self.aiming:
            angle = math.atan2(self.context.avatar.rect.centery - pos[1], self.context.avatar.rect.centerx - pos[0])
            self.fpdy = self.speed * math.sin(angle)
            self.fpdx = self.speed * math.cos(angle)
        else:
            self.fpdy = self.speed
            self.fpdx = 0 
        self.damage = damage
    
    def setfp(self):
        """
        use whenever usual integer rect values are adjusted
        """
        self.fpx = self.rect.centerx
        self.fpy = self.rect.centery
        
    def setint(self):
        """
        use whenever floating point rect values are adjusted
        """
        self.rect.centerx = self.fpx
        self.rect.centery = self.fpy
        
    def update(self):
        self.fpx = self.fpx + self.fpdx
        self.fpy = self.fpy + self.fpdy
        self.setint()
        self.counter = (self.counter + 1) % self.maxcount
        self.image = self.images[self.counter/self.animcycle]
        if not self.context.rect.contains(self.rect):
            self.kill()
        if self.context.currentLevel.finished:
            self.kill()
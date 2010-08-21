#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame

from ..Core import Context

class EnemyRayTemplate(pygame.sprite.Sprite):
    '''
    Ray visual effect
    '''
    context = Context.contextObject
    images = None
    containers = context.bombs, context.obstacles, context.all
    
    ghost = True
    isEvil = True
    
    def __init__(self, emitter, damage, counter=0):
        '''
        Constructor
        '''
        cur = self.images[counter % len(self.images)]
        width = cur.get_width()
        height = self.context.rect.height
        emiHeight = emitter[1]
        
        tracer = pygame.sprite.Sprite()
        tracer.containers = self.context.enemyTracers
        tracer.image = pygame.Surface((width, height), pygame.SRCALPHA)
        tracer.rect = tracer.image.get_rect()
        tracer.rect.center = emitter
        tracer.rect.top = emitter[1]
        tracelist = pygame.sprite.spritecollide(tracer, self.context.player, False)
        for obj in tracelist:
            if emiHeight < obj.rect.top:
                height = obj.rect.top - emiHeight
        
        height += 25
        
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.transform.scale(cur, (cur.get_width(), height), self.image)
        
        self.rect = self.image.get_rect()
        self.rect.center = emitter
        self.rect.top = emitter[1]
        self.damage = damage
        
        self.killOnThisFrame = False
    
    def update(self):
        '''
        Update
        '''
        if self.killOnThisFrame:
            self.kill()
        self.killOnThisFrame = True
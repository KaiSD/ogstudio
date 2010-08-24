#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default enemy module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame, random
from pygame.locals import *

from ..Core import Context

class EnemyTemplate(pygame.sprite.Sprite):
    '''
    Enemy template class
    '''
    context = Context.contextObject
    containers = context.enemies, context.obstacles, context.all
    
    animcycle = 2
    images = None
    
    # Mechanics params
    speed = 1
    attackTreashold = 1
    life = 1
    weapons = []
    damage = 1
    reward = 1
    
    xMove = False
    xMoveChange = False
    xMoveMaxDelay = 1000
    
    yMove = False
    yMoveStay = False
    yMoveMaxDelay = 1000
    
    isEvil = False
    
    def __init__(self, posX=None):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.counter = 0
        self.maxcount = len(self.images)*self.animcycle
        self.rect = self.image.get_rect()
        if 0 <= posX <= 100:
            self.rect.left = posX * (self.context.rect.width - self.rect.width) / 100
        else:
            self.rect.left = random.randrange(self.context.rect.width - self.rect.width)
        self.rect.bottom = self.context.rect.top
        self.rewarded = False
        self.xMoveTimer = 0
        self.yMoveTimer = 0
        
        self.ySpeedMod = 1
        self.appeared = False
        
        self.weaponTicks = 0
                
        if self.xMove:
            self.xSpeed = random.randrange(-self.speed, self.speed)
        else:
            self.xSpeed = 0
            
        if 'Enemies' not in self.context.debug.keys():
            self.context.debug['Enemies'] = 1
        else:
            self.context.debug['Enemies'] += 1
    
    def isDo(self, treashold):
        return not random.randrange(treashold)
    
    def update(self):
        '''
        Update
        '''
        if not self.appeared and self.rect.top > self.context.rect.top:
            self.appeared = True
            if self.yMove:
                self.yMoveTimer = random.randrange(1, self.yMoveMaxDelay)
        
        if self.xMoveChange:
            self.xMoveTimer -= 1
            if self.xMoveTimer <= 0 :
                self.xSpeed = random.randrange(-self.speed, self.speed)
                self.xMoveTimer = random.randrange(1, self.xMoveMaxDelay)
            elif self.rect.left < self.context.rect.left:
                self.xSpeed = random.randrange(0, self.speed)
                self.xMoveTimer = random.randrange(1, self.xMoveMaxDelay)
            elif self.rect.right > self.context.rect.right:
                self.xSpeed = random.randrange(-self.speed, 0)
                self.xMoveTimer = random.randrange(1, self.xMoveMaxDelay)
                

        if self.yMove and self.appeared:
            self.yMoveTimer -= 1
            if self.yMoveTimer <= 0 :
                self.ySpeedMod = random.randrange(-1, 1)
                self.yMoveTimer = random.randrange(1, self.yMoveMaxDelay)
                
        if self.yMoveStay and self.appeared:
            if self.rect.bottom > self.context.rect.bottom:
                self.ySpeedMod = -1
                self.yMoveTimer = random.randrange(1, self.yMoveMaxDelay)
            elif self.rect.top < self.context.rect.top:
                self.ySpeedMod = 1
                self.yMoveTimer = random.randrange(1, self.yMoveMaxDelay)
        
        self.rect.move_ip(self.xSpeed, self.speed*self.ySpeedMod)
        self.counter = (self.counter + 1) % self.maxcount
        self.image = self.images[self.counter/self.animcycle]
        if self.rect.top > self.context.rect.bottom:
            self.kill()
        
        if not len(self.weapons) is 0:
            if self.isDo(self.attackTreashold) and not self.context.currentLevel.finished:
                if self.isEvil:
                    for currentGun in self.weapons:
                        currentGun.fire(self.rect, self.weaponTicks)
                        self.weaponTicks += 1
                        if not currentGun.soundEnd is None:
                            currentGun.soundEnd.set_volume(0.5)
                            currentGun.soundEnd.play()
                else:
                    currentGun = random.choice(self.weapons)
                    currentGun.fire(self.rect, self.weaponTicks)
                    self.weaponTicks += 1
                    if not currentGun.soundEnd is None:
                        currentGun.soundEnd.set_volume(0.5)
                        currentGun.soundEnd.play()
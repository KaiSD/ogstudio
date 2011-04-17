#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype bullet effect module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame
import math

from ..Core import Context

class BulletTemplate(pygame.sprite.Sprite):
    '''
    Explosion visual effect
    '''
    context = Context.contextObject
    images = None
    containers = context.shots, context.all
    reAiming = False
    isRotating = False
    isSwitchTarget = False
    isAccelerating = False
    explosionEffect = None
    maxSpeed = 100
    
    animcycle = 4
    speed = 1
    ghost = False
    
    def __init__(self, pos, damage, offset=0, speedMod=1, target=None, staticRotate=0):
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
        self.target = target
        self.angle = staticRotate
        self.setfp()
        self.aim(target)
        
        if not self.context.debug.has_key('WeaponDamage['+str(self.__class__)+']'):
            self.context.debug['WeaponDamage['+str(self.__class__)+']'] = 0
    
    def aim(self, target):
        if not target is None:
            enemies = self.context.currentLevel.enemiesOnScreen
            if enemies.has_key(target):
                angle = math.atan2(enemies[target][1] - self.rect.center[1], enemies[target][0] - self.rect.center[0])
                self.fpdy = self.speed * math.sin(angle)
                self.fpdx = self.speed * math.cos(angle)
                self.angle = angle+1.57
            elif target is self.context.avatar:
                angle = math.atan2(self.context.avatar.rect.centery - self.rect.center[1], self.context.avatar.rect.centerx - self.rect.center[0])
                self.fpdy = self.speed * math.sin(angle)
                self.fpdx = self.speed * math.cos(angle)
                self.angle = angle+1.57
            elif self.isSwitchTarget:
                if self.context.avatar.aimed:
                    self.context.avatar.aim()
                newTarget = self.context.avatar.target
                if not newTarget == target:
                    self.aim(newTarget)
                else:
                    self.angle = 0
                    target = None
            else:
                self.fpdy = -self.speed*self.speedMod
                self.fpdx = self.offset
                self.angle = 0
                target = None
        else:
            self.fpdy = -self.speed*self.speedMod
            self.fpdx = self.offset
            target = None
        self.target = target
    
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
        '''
        Update
        '''
        if self.reAiming:
            self.aim(self.target)
        self.fpx = self.fpx + self.fpdx
        self.fpy = self.fpy + self.fpdy
        self.setint()
        self.counter = (self.counter + 1) % self.maxcount
        if self.isRotating and not self.angle == 0:
            self.image = pygame.transform.rotate(self.images[self.counter/self.animcycle], -int(self.angle*57))
        else:
            self.image = self.images[self.counter/self.animcycle]
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > self.context.rect.width:
            self.kill()
        if self.rect.top > self.context.rect.height:
            self.kill()
        if self.isAccelerating and self.speed < self.maxSpeed:
            self.speed += 1
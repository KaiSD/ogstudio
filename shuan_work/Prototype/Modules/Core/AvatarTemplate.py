#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default avatar module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame
from pygame.locals import *
from ..Effects.AvatarExplosion import AvatarExplosion
from ..Effects.Explosion import Explosion
from ..Effects.DiedMessage import DiedMessage

from ..Core import Context

class AvatarTemplate(pygame.sprite.Sprite):
    '''
    Player avatar
    '''
    context = Context.contextObject
    images = None
    containers = context.all
    
    #Collision rect
    crect = (0, 0, 0, 0)
    
    #Animation params
    animcycle = 1
    
    #Universal sounds
    soundHit = context.loadSound('hit.wav') 
    
    #Mechanics params
    weaponSlots = []
    gunSlots = []
    heavySlot = (0, 0)
    life = 200
    ammoMod = 1
    reactorMod = 1 
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.counter = 0
        self.maxcount = len(self.images)*self.animcycle
        self.rect = self.image.get_rect()
        self.context.avatar = self
        self.guns = []
        self.weapons = []
        self.heavy = None
        self.soundsToPlay = []
        self.reactor = 0
    
    def weaponsUpdate(self):
        for i in self.weapons+self.guns:
            self.reactor += i.energyCost
        
        reloadMod = 1
        if self.reactor > 100 * self.reactorMod:
            reloadMod = (50 * self.reactorMod + self.reactor) / 50 * self.reactorMod
        
        for i in self.weapons+self.guns:
            i.reloadTime = int(i.reloadTime + reloadMod)
        
        return reloadMod
    
    def update(self):
        self.counter = (self.counter + 1) % self.maxcount
        self.image = self.images[self.counter/self.animcycle]
                
        if self.context.currentLevel.finished:
            self.rect.move_ip(0, -9)
            if self.rect.bottom < self.context.rect.top:
                self.kill()
        else:
            self.rect.center = pygame.mouse.get_pos()
            self.rect = self.rect.clamp(self.context.rect)
        
        # Collision detection
        oldrect = self.rect
        self.rect = Rect(*self.crect)
        self.rect.topleft = (oldrect.left + self.crect[0], oldrect.top + self.crect[1])
        
        collist = pygame.sprite.spritecollide(self, self.context.obstacles, False)
        if collist:
            if self.life - collist[0].damage > 0:
                self.life -= collist[0].damage
                if self.context.enemies in collist[0].containers:
                    Explosion(collist[0])
                    self.context.currentLevel.score += 1
                if not self.soundHit is None:
                    self.soundHit.set_volume(0.2)
                    self.soundHit.play()
            else:
                self.life = 0
                AvatarExplosion(self)
                DiedMessage(self.context)
                self.context.currentLevel.finishTime = self.context.ticks
                self.context.currentLevel.finished = True
                if not self.soundHit is None:
                    self.soundHit.set_volume(0.5)
                    self.soundHit.play()
                self.kill()
            if not collist[0].isEvil:
                collist[0].kill()
        
        # Weapons using
        localSounds = []
        for i in self.weapons + self.guns:
            if i.reloadTimer > 0:
                i.reloadTimer = i.reloadTimer - 1
            firing = pygame.mouse.get_pressed()[0]
            if firing and not self.context.currentLevel.finished:
                if not i.justFired or i.reloadTimer == 0:
                    i.reloadTimer = i.reloadTime
                    if not i.soundLoop is None:
                        if not i.soundLoop in self.soundsToPlay:
                            i.soundLoop.set_volume(0.3)
                            i.soundLoop.play(-1)
                            self.soundsToPlay.append(i.soundLoop)
                    elif not i.soundEnd is None:
                        if not i.soundEnd in localSounds:
                            i.soundEnd.set_volume(0.3)
                            i.soundEnd.play()
                            localSounds.append(i.soundEnd)
                    i.fire(self.rect)
                i.justFired = firing
            elif not i.soundLoop is None:
                if i.soundLoop in self.soundsToPlay:
                    i.soundLoop.stop()
                    self.soundsToPlay.remove(i.soundLoop)
                    if not i.soundEnd is None:
                        i.soundEnd.set_volume(0.3)
                        i.soundEnd.play()
        
        # Heavy weapons
        heavyFiring = pygame.mouse.get_pressed()[2]
        if not self.heavy is None:
            if heavyFiring and (not self.heavy.justFired):
                self.heavy.fire(self.rect)
            self.heavy.justFired = heavyFiring
            if not self.heavy.soundEnd is None:
                self.heavy.soundEnd.set_volume(0.3)
                self.heavy.soundEnd.play()
        
        self.rect = oldrect
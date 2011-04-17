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
    containers = context.all, context.player
    
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
    baseLife = 1
    baseShield = 0
    ammoMod = 1
    reactorMod = 1 
    shieldRegenTime = 30
    
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
        self.life = self.baseLife
        self.shields = self.baseShield
        self.shieldRegenTimer = 0
        self.lastHitSound = 0
        self.weaponTicks = 0
        self.target = None
        self.aimed = False
        
        self.context.debug['EnemyGunHit'] = 0
        self.context.debug['EnemyAimGunHit'] = 0
        self.context.debug['EnemyLaserHit'] = 0
        self.context.debug['DamageGive'] = 0
        
        if not self.context.debug.has_key('WeaponDamage['+str(self.__class__)+']'):
            self.context.debug['WeaponDamage['+str(self.__class__)+']'] = 0
    
    def weaponsUpdate(self):
        for i in self.weapons+self.guns:
            self.reactor += i.energyCost
        
        reloadMod = 1
        
        if self.reactor >= 100 * self.reactorMod:
            reloadMod = (50 * self.reactorMod + self.reactor) / 50 * self.reactorMod
            self.shieldRegenTime += int(3 * (self.reactor - 100 * self.reactorMod))
        else:
            self.shieldRegenTime = 5 + int((self.shieldRegenTime + 300 * self.reactorMod) / (100 * self.reactorMod - self.reactor))
        
        for i in self.weapons+self.guns:
            i.reloadTime = int(i.reloadTime * reloadMod)
            if i.reloadTime > i.maxReloadTime:
                i.reloadTime = i.maxReloadTime
        
        return reloadMod
    
    def aim(self):
        target = self.target
        enemies = self.context.currentLevel.enemiesOnScreen
        posX = self.rect.centerx
        posY = self.rect.top
        if target in enemies: 
            if target.rect.centery < posY:
                return
            else:
                target = None
        dist = 999999
        for i in enemies.keys():
            ep = enemies[i]
            if ep[1] < posY:
                d = (posX - ep[0])+abs(posY - ep[1])/3
                if d < dist:
                    target = i
                    dist = d
        self.target = target
        self.aimed = True
    
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
        
        if self.shieldRegenTimer <= 0:
            self.shields += (self.shields < self.baseShield)
            self.shieldRegenTimer = self.shieldRegenTime
        else:
            self.shieldRegenTimer -= 1
        
        # Collision detection
        localSounds = []
        self.lastHitSound += 1
        oldrect = self.rect
        self.rect = Rect(*self.crect)
        self.rect.topleft = (oldrect.left + self.crect[0], oldrect.top + self.crect[1])
        
        collist = pygame.sprite.spritecollide(self, self.context.obstacles, False)
        if collist:
            if collist[0].__class__.__name__ == "Bullet" or collist[0].__class__.__name__ == "Ray":
                if collist[0].debugName is "EnemyBullet":
                    self.context.debug['EnemyGunHit'] += 1
                elif collist[0].debugName is "EnemyAimingBullet":
                    self.context.debug['EnemyAimGunHit'] += 1
                elif collist[0].debugName is "EnemyRay":
                    self.context.debug['EnemyLaserHit'] += 1
            
            if (self.life + self.shields) - collist[0].damage > 0:
                self.shields -= collist[0].damage
                if self.shields < 0:  
                    self.life += self.shields
                    self.shields = 0
                if self.context.enemies in collist[0].containers:
                    Explosion(collist[0])
                    self.context.currentLevel.score += 1
                if not self.soundHit is None and self.lastHitSound > 10:
                    self.soundHit.set_volume(0.2)
                    self.soundHit.play()
                    self.lastHitSound = 0
            else:
                self.life = 0
                self.shields = 0
                AvatarExplosion(self)
                DiedMessage(self.context)
                self.context.currentLevel.finishTime = self.context.ticks
                self.context.currentLevel.finished = True
                if not self.soundHit is None and self.lastHitSound > 10:
                    self.soundHit.set_volume(0.5)
                    self.soundHit.play()
                    self.lastHitSound = 0
                self.kill()
            if not collist[0].isEvil:
                collist[0].kill()
        
        # Weapons using
        self.aim()
        for i in self.weapons + self.guns:
            if i.reloadTimer > 0:
                i.reloadTimer = i.reloadTimer - 1
            firing = pygame.mouse.get_pressed()[0]
            if firing and not self.context.currentLevel.finished:
                self.context.debug['DamageGive'] += i.damage
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
                    i.fire(self.rect, self.weaponTicks)
                    self.weaponTicks += 1
                    i.keepTimer = i.keepFire
                elif not i.justFired or i.keepTimer > 0:
                    i.fire(self.rect, self.weaponTicks)
                    self.weaponTicks += 1
                    i.keepTimer -= 1
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
            if heavyFiring and not (self.heavy.justFired or self.heavy.reloadTimer > 0):
                self.heavy.fire(self.rect)
                self.heavy.reloadTimer = self.heavy.reloadTime 
            self.heavy.justFired = heavyFiring
            if self.heavy.reloadTimer > 0:
                self.heavy.reloadTimer -= 1
            if not self.heavy.soundEnd is None:
                self.heavy.soundEnd.set_volume(0.3)
                self.heavy.soundEnd.play()
                
        self.rect = oldrect
        self.aimed = False
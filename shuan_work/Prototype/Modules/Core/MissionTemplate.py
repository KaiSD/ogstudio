#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission root module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame, os, random

from ..Effects.WinMessage import WinMessage
from ..Effects.Explosion import Explosion
from ..Effects.BigDamagingExplosion import Explosion as BigDamagingExplosion
from ..Effects import BossMessage

import Context

class MissionTemplate(object):
    '''
    Shuan gameplay slice prototype mission root class
    '''
    name = ''
    context = Context.contextObject
    speed = 1
    landTexture = ''
    music = ''
    sequence = ()
    
    boss = None
    bossMeter = None
    
    def __init__(self):
        '''
        Constructor
        '''
        filename = self.landTexture + str(self.context.rect.width) + '.png'
        print 'Loading image: ', filename
        background = pygame.image.load(os.path.join('data', filename)).convert()
        self.tileSide = background.get_height()
        self.counter = 0
        self.sequenceEntry = 0
        self.sequenceFrame = 0
        self.sequenceNextFrame = 0
        self.land = pygame.Surface((self.context.rect.width, self.context.rect.height + self.tileSide)).convert()
        self.startTime = pygame.time.get_ticks()
        self.finished = False
        self.win = False
        self.finishTime = 0
        self.enemiesOnScreen = {}
        
        if len(self.music) > 0:
            filename = self.music + '.mp3'
            print 'Loading music track: ', filename
            self.context.playMusic(filename)
        
        for x in range(self.context.rect.width/self.tileSide):
            for y in range(self.context.rect.height/self.tileSide + 1):
                self.land.blit(background, (x*self.tileSide, y*self.tileSide))
        
        self.score = 0
        
        self.context.debug['DamageTakenByEnemies'] = 0
        
        self.context.currentLevel = self
        
    def offset(self):
        '''
        Returns background offset
        '''
        self.counter = (self.counter - self.speed) % self.tileSide
        return (0, self.counter, self.context.rect.width, self.context.rect.height)
    
    def objectives(self):
        '''
        Level objectives.
        Checking every update. Must return True when mission is complete.
        Implement your objectives. Default mission is incompletable.
        '''
        return False
    
    def getTimer(self):
        return pygame.time.get_ticks() - self.startTime
    
    def update(self):
        '''
        Mission is going on
        '''
        # Check if we're done
        if self.finished:
            return
        
        # Mission commands
        def commandWait(params):
            self.sequenceNextFrame += params[0]*6
        
        def commandWaitKill(params):
            if not self.boss is None:
                if self.boss.life <= 0:
                    self.bossMeter.kill()
                else:
                    self.sequenceEntry -= 1
        
        def commandSpawnBoss(params):
            self.boss = params[0].Enemy(50)
            self.bossMeter = BossMessage.BossMessage(self.context)
        
        def commandRandomEnemies(params):
            for i in xrange(0, params[0]):
                random.choice(params[1:]).Enemy()
        
        def commandSpawn(params):
            if len(params) > 1:
                params[0].Enemy(params[1])
            else:
                params[0].Enemy()
        
        def commandSetSpeed(params):
            self.speed = params[0]
        
        def commandDebug(params):
            print params[0]
        
        MissionCommands = {
                           'Wait':commandWait,
                           'WaitBossKill':commandWaitKill,
                           'RandomEnemies':commandRandomEnemies,
                           'Spawn':commandSpawn,
                           'Boss':commandSpawnBoss,
                           'Speed':commandSetSpeed,
                           'Debug':commandDebug
        }
        
        # Keep going
        if self.sequenceFrame == self.sequenceNextFrame:
            if self.sequenceEntry < len(self.sequence):
                command = self.sequence[self.sequenceEntry]
                MissionCommands[command[0]](command[1:])
                self.sequenceNextFrame += 1
                self.sequenceEntry += 1
            else:
                self.finished = True
        
        # Killing time
        collist = pygame.sprite.groupcollide(self.context.shots, self.context.enemies, False, False)
        for shot in collist.keys():
            if not shot.explosionEffect is None:
                shot.explosionEffect(collist[shot][0], shot.damage/2)
            enemy = collist[shot][0]
            if enemy.life > shot.damage:
                enemy.life -= shot.damage
                self.context.debug['DamageTakenByEnemies'] += shot.damage
                self.context.debug['WeaponDamage['+str(shot.__class__)+']'] += shot.damage
            else:
                enemy.life -= shot.damage
                self.context.debug['DamageTakenByEnemies'] += shot.damage
                self.context.debug['WeaponDamage['+str(shot.__class__)+']'] += shot.damage
                if not enemy.rewarded:
                    enemy.kill()
                    Explosion(collist[shot][0])
                    self.score += enemy.reward
                    enemy.rewarded = True
            if not shot.ghost:
                shot.kill()
        
        if self.finished:
            WinMessage(self.context)
            self.finishTime = self.getTimer()
            self.win = True
        
        self.sequenceFrame += 1
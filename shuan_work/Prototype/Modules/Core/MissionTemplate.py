#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission root module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame, os, random

from ..Effects.WinMessage import WinMessage
from ..Effects.Explosion import Explosion

import Context

class MissionTemplate(object):
    '''
    Shuan gameplay slice prototype mission root class
    '''
    name = ''
    context = Context.contextObject
    speed = 1
    landTexture = ''
    def __init__(self):
        '''
        Constructor
        '''
        filename = self.landTexture + str(self.context.rect.width) + '.png'
        print 'Loading image: ', filename
        background = pygame.image.load(os.path.join('data', filename)).convert()
        self.tileSide = background.get_height()
        self.counter = 0
        self.land = pygame.Surface((self.context.rect.width, self.context.rect.height + self.tileSide)).convert()
        self.startTime = pygame.time.get_ticks()
        self.finished = False
        
        for x in range(self.context.rect.width/self.tileSide):
            for y in range(self.context.rect.height/self.tileSide + 1):
                self.land.blit(background, (x*self.tileSide, y*self.tileSide))
        
        self.score = 0
        
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
    
    def randomSpawner(self, treshold, *enemies):
        if not random.randrange(treshold) and not self.finished:
            random.choice(enemies)()
    
    def update(self):
        '''
        Level update. Doing nothing right now. Implement it yourself.
        Don't forget to call self.finishUpdate() in the end, otherwise your enemies will ignore your fires.
        '''
        
        #If you are going to rewrite the update method, don's forget to add this call in the end.
        self.finishUpdate()
    
    def getTimer(self):
        return pygame.time.get_ticks() - self.startTime
    
    def finishUpdate(self):
        '''
        Method to check collisions and kill people. Call it in the end of your mission's update() method.
        '''
        if self.finished:
            return
        
        collist = pygame.sprite.groupcollide(self.context.shots, self.context.enemies, False, False)
        for shot in collist.keys():
            enemy = collist[shot][0]
            if enemy.life > shot.damage:
                enemy.life -= shot.damage
            else:
                if not enemy.rewarded:
                    enemy.kill()
                    Explosion(collist[shot][0])
                    self.score += enemy.reward
                    enemy.rewarded = True
            if not shot.ghost:
                shot.kill()
        
        if self.objectives():
            WinMessage(self.context)
            self.finished = True
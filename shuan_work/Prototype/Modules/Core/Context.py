#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype context module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame, os
import TextRenderer
from pygame.locals import *

class Context:
    '''
    Context
    '''
    obj = None
    def __new__(cls,*dt,**mp):
        '''
        Singleton checker
        '''
        if cls.obj is None:
            cls.obj = object.__new__(cls,*dt,**mp)
        return cls.obj
    
    def __init__(self):
        '''
        Constructor
        '''
        self.shots = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.tracers = pygame.sprite.Group()
        self.enemyTracers = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        
        self.backObjects = pygame.sprite.RenderPlain()
        self.ui = pygame.sprite.RenderPlain()
        self.all = pygame.sprite.RenderPlain()
        
        self.rect = None
        self.currentLevel = None
        self.avatar = None
        
        # Profiling
        self.time = 0
        self.ticks = 0
        self.timestamp = 0
        
        # Resources
        self.spriteAlbums = {}
        self.fonts = {}
        self.sound = {}
        self.debug = {}
    
    def loadSprite(self, filename, *rects):
        '''
        Loads and returns sprite from given filename and rect. Retusns list of images if 
        '''
        album = None
        if filename in self.spriteAlbums.keys():
            album = self.spriteAlbums[filename]
        else:
            print 'Loading image: ', filename
            filename = os.path.join('data', filename)
            album = pygame.image.load(filename)
            self.spriteAlbums[filename] = album
        
        if len(rects) > 0:
            if type(rects[0]) is list:
                imgs = []
                for rect in rects[0]:
                    rect = Rect(rect)
                    image = None
                    image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
                    image.blit(album, (0, 0), rect)
                    imgs.append(image)
                return imgs
            else:
                rect = Rect(rects[0])
                image = None
                image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
                image.blit(album, (0, 0), rect)
                return image
        else:
            return album.sheet
    
    def loadText(self, font, size, text, color):
        '''
        Loads font and creates an image with selected text and color
        '''
        key = font+str(size)
        if not key in self.fonts.keys():
            print 'Loading font: ', font
            fontRenderer = TextRenderer.TextRenderer(font, size)
            self.fonts[font+str(size)] = fontRenderer
        return self.fonts[key].getImage(text, color)
    
    def loadSound(self, filename):
        '''
        Loads a sound
        '''
        if not filename in self.sound.keys():
            print 'Loading sound: ', filename
            filename = os.path.join('data', filename)
            self.sound['filename'] = pygame.mixer.Sound(filename)
        return self.sound['filename']
    
    def profStart(self):
        self.timestamp = pygame.time.get_ticks()
    
    def profEnd(self):
        self.time += pygame.time.get_ticks() - self.timestamp
    
    def tick(self):
        self.ticks += 1

contextObject = Context()
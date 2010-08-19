#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame
from pygame.locals import *

import Context

class WeaponTemplate(object):
    '''
    Weapon class
    '''
    context = Context.contextObject
    reloadTime = 0
    damage = 0
    soundLoop = None
    soundStart = None
    soundEnd = None
    ammo = 0

    def __init__(self, posX, posY):
        '''
        Constructor
        '''
        self.reloadTimer = 0
        self.justFired = 0
        
        self.posX = posX
        self.posY = posY
        
        self.ammo = int(self.ammo * self.context.avatar.ammoMod)
    
    def fire(self, rect):
        '''
        Fires a gun. Don't forget to implement your own fire method, or your gun will not fire at all.
        '''
        pass
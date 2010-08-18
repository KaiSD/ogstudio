#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype sprite album module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pygame
from pygame.locals import *

class TextRenderer:
    '''
    Text renderer class
    '''
    def __init__(self, fontName, fontSize):
        '''
        Constructor
        '''
        self.font = pygame.font.SysFont(fontName, fontSize)
        
    def getImage(self, text, color):
        '''
        Returns image from given rect
        '''
        return self.font.render(text, 1, color)

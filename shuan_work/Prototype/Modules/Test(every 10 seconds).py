#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission root module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from Enemies import Enemy1
from Effects import BossMessage

from .Core.MissionTemplate import MissionTemplate

class Mission(MissionTemplate):
    '''
    Shuan gameplay slice prototype mission root class
    '''
    name = 'Simple Mission'
    speed = 2
    landTexture = 'mars'
    
    boss = None
    bossMeter = None
    
    music = ''
    
    sequence = (
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                ('Wait',100),
                ('Spawn', Enemy1, 50),
                )
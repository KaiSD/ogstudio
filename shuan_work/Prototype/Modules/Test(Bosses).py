#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission root module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from Enemies import Boss1, Boss2
from Effects import BossMessage

from .Core.MissionTemplate import MissionTemplate

class Mission(MissionTemplate):
    '''
    Shuan gameplay slice prototype mission root class
    '''
    name = 'Simple Mission'
    speed = 2
    landTexture = 'mars'
    music = 'Dirty_Road_Blues'
    
    sequence = (
                ('Wait',5),
                ('Boss',Boss1),
                ('Speed', 1),
                ('Wait',1),
                ('Speed', 0),
                ('WaitBossKill', ),
                ('Speed', 1),
                ('Wait',1),
                ('Speed', 2),
                ('Wait',1),
                ('Speed', 3),
                ('Wait',5),
                ('Boss',Boss2),
                ('WaitBossKill', ),
                )
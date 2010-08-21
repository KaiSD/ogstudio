#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default enemy module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EnemyTemplate import EnemyTemplate

from ..EnemyWeapons.EnemyGun import Weapon as Gun 

class Enemy(EnemyTemplate):
    '''
    Standart Enemy
    '''
    images = EnemyTemplate.context.loadSprite('enemy3.png', [(0, 0, 29, 24)])

    # Mechanics params
    speed = 1
    attackTreashold = 10000
    life = 600
    weapons = []
    damage = 150
    
    xMove = True
    xMoveChange = True
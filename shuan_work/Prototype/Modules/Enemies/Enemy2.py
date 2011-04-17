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
    images = EnemyTemplate.context.loadSprite('enemy2.png', [(0, 0, 33, 34)])

    # Mechanics params
    speed = 4
    attackTreashold = 100
    life = 162
    weapons = [Gun(16, 19)]
    damage = 80
    
    xMove = True
    xMoveChange = True
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default enemy module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.EnemyTemplate import EnemyTemplate

from ..EnemyWeapons.EnemyAimGun import Weapon as Gun 

class Enemy(EnemyTemplate):
    '''
    Standart Enemy
    '''
    images = EnemyTemplate.context.loadSprite('enemy1.png', [(0, 0, 27, 26),
                                                            (27, 0, 27, 26)])

    # Mechanics params
    speed = 3
    attackTreashold = 250
    life = 100
    weapons = [Gun(16, 19)]
    damage = 20
    
    xMove = True
    xMoveChange = True

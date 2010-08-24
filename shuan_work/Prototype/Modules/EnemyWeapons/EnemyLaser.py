#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default weapon module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.WeaponTemplate import WeaponTemplate
from ..Bullets.EnemyRay import Ray

class Weapon(WeaponTemplate):
    '''
    Enemy gun
    '''
    reloadTime = 0
    damage = 1

    def __init__(self, posX, posY):
        '''
        Constructor
        '''
        self.reloadTimer = 0
        self.justFired = 0
        
        self.posX = posX
        self.posY = posY
        
        if not 'EnemyLaser' in self.context.debug.keys():  
            self.context.debug['EnemyLaser'] = 0 
    
    def fire(self, rect, counter=0):
        Ray((rect.left + self.posX, rect.top + self.posY), self.damage, counter)
        self.context.debug['EnemyLaser'] += 1
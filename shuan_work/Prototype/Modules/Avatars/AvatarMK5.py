#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype mission default avatar module

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ..Core.AvatarTemplate import AvatarTemplate

class Avatar(AvatarTemplate):
    '''
    Player avatar
    '''
    images = AvatarTemplate.context.loadSprite('avatarShip.png', [(0, 0, 57, 57),
                                                                  (57, 0, 57, 57),
                                                                  (114, 0, 57, 57)])
    crect = (0, 22, 57, 29)
    gunSlots = [(23, 0), (34, 0)]
    weaponSlots = [(6, 7), (16, 5), (28, 10), (40, 5), (50, 7)]
    heavySlot = (28, 26)
    baseLife = 200
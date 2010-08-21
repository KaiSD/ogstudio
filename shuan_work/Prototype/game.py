#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay slice prototype

(c) 2010 Opensource Game Studio Team (http://opengamestudio.org)
'''

import os, pygame
import config
from pygame.locals import *

from Modules.Effects import HealthMessage, ScoreMessage, AmmoMessage, ReactorMessage

from Modules.Core import Context

VERSION = 0.75
NAME = 'Shuan gameplay slice prototype'

def main(**args):
    pygame.mixer.init(44100, -16, 2, 512)
    pygame.init()
    
    context = Context.contextObject
    context.rect = Rect(0, 0, config.screenWidth, config.screenHeight)
    
    winstyle = 0
    bestdepth = pygame.display.mode_ok(context.rect.size, winstyle, 32)
    screen = pygame.display.set_mode(context.rect.size, winstyle, bestdepth)
    
    # decorate the game window
    pygame.mouse.set_visible(False)
    
    if 'mission' in args:
        config.mission = args['mission']
    if 'playerShip' in args:
        config.playerShip = args['playerShip']
    if 'playerWeapons' in args:
        config.playerWeapons = args['playerWeapons']
    if 'playerGun' in args:
        config.playerGun = args['playerGun']
    if 'playerHeavyWeapon' in args:
        config.playerHeavyWeapon = args['playerHeavyWeapon']
    if 'playerShield' in args:
        config.playerShield = args['playerShield']
    if 'playerAmmo' in args:
        config.playerAmmo = args['playerAmmo']
    if 'playerReactor' in args:
        config.playerReactor = args['playerReactor']
    
    # some game init code here
    level = __import__('Modules.'+config.mission, globals(), locals(), ['Mission'], -1).Mission()
    pygame.display.set_caption(NAME + ' '+str(VERSION)+': '+level.name)
    player = __import__('Modules.Avatars.'+config.playerShip, globals(), locals(), ['Avatar'], -1).Avatar()
    
    player.baseShield = int(player.baseLife * float(config.playerShield) / 4)
    player.ammoMod *= 1 + float(config.playerAmmo) / 2
    player.reactorMod *= 1 + float(config.playerReactor) / 2
    player.reactor += player.baseShield / 2 + int(config.playerAmmo) * 10
    
    weaponCounter = 0
    for i in config.playerWeapons:
        if len(player.weaponSlots) > weaponCounter:
            weapon = __import__('Modules.Weapons.'+i, globals(), locals(), ['Weapon'], -1).Weapon(player.weaponSlots[weaponCounter][0], player.weaponSlots[weaponCounter][1], weaponCounter - len(player.weaponSlots) / 2)
            print weaponCounter - len(player.weaponSlots) / 2
            player.weapons.append(weapon)
            weaponCounter += 1
    
    weaponCounter = 0
    for i in player.gunSlots:
        gun = __import__('Modules.Guns.'+config.playerGun, globals(), locals(), ['Weapon'], -1).Weapon(player.gunSlots[weaponCounter][0], player.gunSlots[weaponCounter][1], weaponCounter * 2 - len(player.gunSlots) / 2)
        player.guns.append(gun)
        weaponCounter += 1
    
    player.heavy = __import__('Modules.HeavyWeapons.'+config.playerHeavyWeapon, globals(), locals(), ['Weapon'], -1).Weapon()
    
    energy = int(player.weaponsUpdate())
    player.baseShield -= energy*(energy < 0)
    player.baseShield *= (player.baseShield > 0)
    player.shields = player.baseShield
    
    HealthMessage.HealthMessage(context)
    ScoreMessage.ScoreMessage(context)
    AmmoMessage.AmmoMessage(context)
    ReactorMessage.ReactorMessage(context, energy)
    
    clock = pygame.time.Clock()
    
    while 1:
        context.profStart()
        # get input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print '-------------------------------------------------------------------'
                print 'Average time consuming: ', float(context.time) / float(context.ticks), 'ms/frame.'
                print 'Average FPS: ', float(context.ticks)/float(context.time) * 1000
                print '-------------------------------------------------------------------'
                statfile = os.path.join('stat', 'missions.csv')
                if not 'missions.csv' in os.listdir('stat'):
                    f = open(statfile, 'w')
                    prev = ''
                else:
                    f = open(statfile, 'r')
                    prev = f.read()
                    f.close()
                    f = open(statfile, 'w')
                report = (level.name,
                          config.playerShip,
                          config.playerShield,
                          config.playerReactor,
                          config.playerAmmo,
                          config.playerGun,
                          config.playerWeapons,
                          config.playerHeavyWeapon,
                          level.finishTime / 1000,
                          level.win,
                          level.score,
                          player.life,
                          player.heavy.ammo)
                text = '%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n' % report
                f.write(prev+text)
                f.close()
                return
        keystate = pygame.key.get_pressed()
        
        pygame.display.flip()
        # update all the sprites
        context.all.update()
        context.ui.update()
        level.update()

        # draw the scene
        screen.blit(level.land, (0, 0), level.offset())
        context.backObjects.draw(screen)
        context.all.draw(screen)
        context.ui.draw(screen)
        pygame.display.flip()
        context.tick()
        context.profEnd()
        # cap the framerate
        clock.tick(60)
    

if __name__ == '__main__':
    main()

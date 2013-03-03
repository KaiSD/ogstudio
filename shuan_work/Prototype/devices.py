#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype core module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from core import *

'''
ENEMY WEAPONS
'''
class EnemyGun(WeaponKind):
    type = PROJECTILE
    image = 'data/graphics/ebullet1.png'
    position = 0, 0
    damage = 1
    velocity = 0, -1000
    isGood = False
    lifetime = 1
    startSound = 'data/sounds/enemy_shot.wav'

class EnemyLaser(WeaponKind):
    type = RAY
    image = 'data/graphics/yellowray.png'
    damage = 2
    isGood = False
    anchor = 8, 0
    rotation = 180

class EnemySpawnAimer(WeaponKind):
    type = SPAWN
    spawnID = 'Aimer'

class EnemySpawnKami(WeaponKind):
    type = SPAWN
    spawnID = 'Kami'

class EnemyShieldProjector(WeaponKind):
    class LocalKind(EffectKind):
        name = "Defended"
        distance = 200
        
        def start(self, instance):
            target = instance.target
            target.shields += 10
            target.shieldsRegen += 1
            target.playShield(1)
            print self, target
        
        def check(self, instance):
            if instance.source._gonnaDie == True:
                return False
            s = instance.source.position
            t = instance.target.position
            return (s[0] - t[0])**2 + (s[1] - t[1])**2 <= self.distance**2 
        
        def end(self, instance):
            instance.shields -= 10
            instance.shieldsRegen -= 1            
            if instance.shields == 0:
                instance.playShield(-1)
        
    type = AURA
    runner = LocalKind()
    
'''
AVATAR WEAPONS
'''
class Empty(WeaponKind):
    type = EMPTY
    name = "None"
    energy = 0
    energyIdle = 0

class Minigun(WeaponKind):
    type = PROJECTILE
    image = 'data/graphics/bullet1.png'
    position = 0, 10
    damage = 2
    isGood = True
    velocity = 0, 1600
    lifetime = 0.5
    pof = 0.1
    loopSound = 'data/sounds/minigun_loop.wav'
    endSound = 'data/sounds/minigun_end.wav'
    soundVolume = 0.3
    name = "Minigun"

class Laser(WeaponKind):
    type = RAY
    image = 'data/graphics/blueray.png'
    damage = 2
    isGood = True
    anchor = 8, 16
    rotation = 0
    loopSound = 'data/sounds/laser_loop.wav'
    endSound = 'data/sounds/laser_end.wav'
    soundVolume = 0.6
    name = "Laser"

class Turret(WeaponKind):
    type = TURRET
    image = 'data/graphics/bullet2.png'
    position = 0, -5
    damage = 2
    isGood = True
    velocity = 0, 1000
    lifetime = 1
    pof = 0.15
    name = "Turret"

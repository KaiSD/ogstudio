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
class EnemyGun(DeviceKind):
    type = PROJECTILE
    image = 'data/graphics/ebullet1.png'
    position = 0, 0
    damage = 1
    velocity = 0, -1000
    isGood = False
    lifetime = 1
    startSound = 'data/sounds/enemy_shot.wav'

class EnemyLaser(DeviceKind):
    type = RAY
    image = 'data/graphics/yellowray.png'
    damage = 2
    isGood = False
    anchor = 8, 0
    rotation = 180

class EnemySpawnAimer(DeviceKind):
    type = SPAWN
    spawnID = 'Aimer'

class EnemySpawnMine(DeviceKind):
    type = SPAWN
    spawnID = 'DumbMine'

class EnemyShieldProjector(DeviceKind):
    class LocalKind(EffectKind):
        name = "Defended"
        distance = 200
        
        def start(self, instance):
            target = instance.target
            target.shields += 10
            target.shieldsRegen += 1
            target.playShield(1)
        
        def check(self, instance):
            if instance.source._gonnaDie:
                return False
            s = instance.source.position
            t = instance.target.position
            return (s[0] - t[0])**2 + (s[1] - t[1])**2 <= self.distance**2 
        
        def end(self, instance):
            target = instance.target
            target.shields -= 10
            target.shieldsRegen -= 1            
            if target.shields == 0:
                target.playShield(-1)
        
    type = AURA
    runner = LocalKind()
    
'''
AVATAR WEAPONS
'''
class Empty(DeviceKind):
    type = EMPTY
    name = "None"
    energy = 0
    energyIdle = 0

class Minigun(DeviceKind):
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

class Laser(DeviceKind):
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

class Turret(DeviceKind):
    type = TURRET
    image = 'data/graphics/bullet2.png'
    position = 0, -5
    damage = 2
    isGood = True
    velocity = 0, 1000
    lifetime = 1
    pof = 0.15
    name = "Turret"

'''
AVATAR DEVICES
'''
class Recharger(DeviceKind):
    class LocalKind(EffectKind):
        name = "Recharge"
        duration = 2
        
        def start(self, instance):
            target = instance.target
            for i in target.runners:
                if i.group == EGNOSHIELDS:
                    i.timeToDie = True
            target.playShield(1)
        
        def check(self, instance):
            if instance.target.absorbedDamage == 0:
                return False
            else:
                return True
        
        def effect(self, target):
            if target.absorbedDamage > 0:
                target.absorbedDamage -= 1
    
    type = EFFECT
    name = "Recharger"
    runner = LocalKind()

class RocketLauncher(DeviceKind):
    type = TURRET
    image = loadAnimation('data/graphics/rocket.png', 3, 1, 0.1, True)
    position = 0, -5
    damage = 50
    isGood = True
    rotation = True
    keepTarget = True
    velocity = 0, 500
    lifetime = 2
    name = "Rockets"

class Swarm(DeviceKind):
    type = PROJECTILE
    image = loadAnimation('data/graphics/rocket.png', 3, 1, 0.1, True)
    position = 0, -5
    damage = 20
    isGood = True
    velocity = 0, 500
    lifetime = 0.5
    name = "Swarm"
    directions = 20
    spread = 45
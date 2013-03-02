#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype core module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from cocos import menu, layer, scene, scenes, text, sprite, actions, collision_model, euclid
import math
import random
import copy
from helpers import *

'''
CONSTANTS
'''
EMPTY = -1
PROJECTILE = 0
RAY = 1
TURRET = 2

'''
ACTION CLASSES
'''
class ActionDie(actions.InstantAction):
    def start(self):
        self.target.kill()

class ActionShoot(actions.InstantAction):
    def start(self):
        self.target.shoot()

class ActionAimAndShoot(actions.InstantAction):
    def start(self):
        self.target.shoot(True)

class ActionStopShooting(actions.InstantAction):
    def start(self):
        self.target.stopShooting()

class ActionRandomMovement(actions.IntervalAction ):
    def init( self, duration ):
        self.duration = duration
        self.initial = None
        self.destination = None

    def update( self, t ):
        if self.initial == None:
            self.initial = self.target.position
            self.destination = rel(random.random(), random.random())
        x = self.initial[0] + (self.destination[0] - self.initial[0]) * t
        y = self.initial[1] + (self.destination[1] - self.initial[1]) * t
        self.target.position = x,y

class ActionFadeTimescale(actions.IntervalAction ):
    '''
    WARNING: Use it for ASprite and it's subclasses only
    '''
    def init( self, ts, duration ):
        self.duration = duration
        self.originalTs = None
        self.ts = ts

    def update( self, t ):
        if self.originalTs == None:
            self.originalTs = self.target.timeScale
        ts = self.originalTs + (self.ts - self.originalTs) * t
        self.target.setTimeScale(ts)

'''
KINDS
'''
class WeaponKind(object):
    position = 0, 9
    damage = 2
    energy = 20
    energyIdle = 5 
    damageToShieldsMod = 1
    isGood = True
    name = "Weapon"
    
    type = PROJECTILE
    # Projectile and turret params
    velocity = 0, 1600
    lifetime = 0.5
    pof = 1
    
    # Ray params
    anchor = 0, 0
    rotation = 0
    
    startSound = None
    loopSound = None
    endSound = None
    soundVolume = 0.5
    
    def __init__(self, dx=0, dy=0):
        super(WeaponKind, self).__init__()
        self.position = self.position[0] + dx, self.position[1] + dy 
        if not self.startSound is None:
            self.startSound = loadSound(self.startSound, self.soundVolume)
        if not self.endSound is None:
            self.endSound = loadSound(self.endSound, self.soundVolume)
        if not self.loopSound is None:
            self.loopSound = loadSound(self.loopSound, self.soundVolume) 

class AvatarKind(object):
    image = loadAnimation('data/graphics/avatarShip.png', 3, 1, 0.1, True)
    life = 100
    engine = 1
    weapons = ()
    weaponSlots = ()
    deviceSlots = ()
    name = 'Avatar'
    
    def __init__(self):
        super(AvatarKind, self).__init__()

class EnemyKind(object):
    image = loadAnimation('data/graphics/enemy1.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    actions = actions.MoveBy((0,-900),duration=6) + ActionDie()
    weapons = ()

    def __init__(self):
        super(EnemyKind, self).__init__()
    
    def switchBrains(self, idx):
        pass

class EffectKind(object):
    def __init__(self):
        super(EffectKind, self).__init__()

'''
TS-SPRITE CLASS
'''
class ASprite(sprite.Sprite):
    class ActionScalableInterval(actions.Action):
        def init(self, one, ts=1):
            self.one = one
            self.timeScale = ts
    
        def start(self):
            self.current_action = copy.deepcopy(self.one)
            self.current_action.target = self.target
            self.current_action.start()
    
        def step(self, dt):
            self._elapsed += dt*self.timeScale
            self.current_action.step(dt*self.timeScale)
            if self.current_action.done():
                self.current_action.stop()
                self._done = True
    
        def stop(self):
            if not self._done:
                self.current_action.stop()
        
        def setTimeScale(self, ts):
            self.timeScale = ts
    
    def __init__(self, *args):
        super(ASprite, self).__init__(*args)
        self.timeScale = 1
    
    def do(self, action):
        new = self.ActionScalableInterval(action, self.timeScale)
        super(ASprite, self).do(new)
    
    def doUnscaled(self, action):
        super(ASprite, self).do(action)
    
    def setTimeScale(self, ts):
        self.timeScale = ts
        for j in self.actions:
            if issubclass(j.__class__, self.ActionScalableInterval):
                j.setTimeScale(ts)

'''
ELEMENT CLASSES
'''
class Bullet(ASprite):
    def __init__(self, owner, kind, target=None):
        super(Bullet, self).__init__(kind.image)
        self.position = owner.position[0] + kind.position[0], owner.position[1] + kind.position[1]
        self.damage = kind.damage
        self.velocity = kind.velocity
        self.isGood = kind.isGood
        lifetime = kind.lifetime
        
        self.layer = owner.owner
        
        if self.isGood:
            self.layer.avatarBullets.append(self)
        else:
            self.layer.enemyBullets.append(self)
        
        if not target is None:
            self.aim(target)
        
        self.layer.add(self, z=5)
        self.do(actions.Move() | actions.Delay(lifetime) +  ActionDie())
    
    def aim(self, target):
        speed = abs(self.velocity[1])
        angle = math.atan2(target.position[1] - self.position[1], target.position[0] - self.position[0])
        dy = speed * math.sin(angle)
        dx = speed * math.cos(angle)
        self.velocity = dx, dy
    
    def kill(self):
        if self.isGood:
            self.layer.avatarBullets.remove(self)
#            self.layer.cmae.remove_tricky(self)
        else:
            self.layer.enemyBullets.remove(self)
#            self.layer.cmea.remove_tricky(self)
        super(Bullet, self).kill()

class Ray(ASprite):
    def __init__(self, owner, kind):
        super(Ray, self).__init__(kind.image)
        self.image_anchor = kind.anchor
        self.rotation = kind.rotation
        self.offset = (kind.position[0], kind.position[1])
        self.position = owner.position[0] + kind.position[0], owner.position[1] + kind.position[1]
        self.damage = kind.damage
        self.isGood = kind.isGood
        self.layer = owner.owner
        self.owner = owner
        self.timeScale = owner.timeScale
        if self.isGood:
            self.layer.avatarRay.append(self)
        else:
            self.layer.enemyRay.append(self)
        
        self.layer.add(self, z=2)
    
    def kill(self):
        if self.isGood:
            self.layer.avatarRay.remove(self)
        else:
            self.layer.enemyRay.remove(self)
            self.owner.rays.remove(self)
        super(Ray, self).kill()

class Avatar(ASprite):
    def __init__(self, owner, kind):
        self.settings = Settings()
        super(Avatar, self).__init__(kind.image)
        self.owner = owner
        self.life = kind.life
        self.shields = 0
        self.shiendsRegen = 0
        self.absorbedDamage = 0.0
        self.takenDamage = 0
        self.weapons = ()
        self._wSlots = kind.weaponSlots
        self._dSlots = kind.deviceSlots
        self.engine = kind.engine
        self.consume = 0
        self.hp = self.life
        self.sp = self.shields
        self.schedule_interval(self.regen, 0.1)
    
    def setup(self, gunsList, weaponsList, devicesList, shieldsList, enginesList, reactorList):
        settings = self.settings
        self.shields = shieldsList[settings.avatarShields][1]
        self.shiendsRegen = shieldsList[settings.avatarShields][2]
        self.engine = enginesList[settings.avatarEngine][1]
        self.reactor = reactorList[settings.avatarReactor][1]
        self.consume = enginesList[settings.avatarEngine][2] + shieldsList[settings.avatarShields][3]
        weapons = []
        if len(self._wSlots) >= 1:
            weapons.append(gunsList[settings.avatarGun](self._wSlots[0]))
            self.consume += gunsList[settings.avatarGun].energyIdle
        if len(self._wSlots) >= 2:
            weapons.append(gunsList[settings.avatarGun](self._wSlots[1]))
            self.consume += gunsList[settings.avatarGun].energyIdle
        for i in self.settings.avatarWeapons:
            if len(weapons) < len(self._wSlots):
                weapons.append(weaponsList[i](self._wSlots[len(weapons)]))
                self.consume += weaponsList[i].energyIdle
        self.weapons = tuple(weapons)
        
    
    def takeDamage(self, damage, damageToShieldsMod=1):
        if self.shields - self.absorbedDamage > 0:
            self.absorbedDamage += damage
            if self.absorbedDamage > self.shields:
                  self.takenDamage += self.absorbedDamage - self.shields
                  self.absorbedDamage = self.shields
        else:
            self.takenDamage += damage
        
        if self.takenDamage > self.life:
            self.owner.killAvatar()
        
        self.hp = self.life - self.takenDamage
        self.sp = self.shields - self.absorbedDamage
    
    def regen(self, *args):
        modShields = 1.0
        modSpeed = 1.0
        
        rc = self.consume * 100 / self.reactor
        
        if rc < 80:
            modShields = modShields * 80 / rc
            modSpeed = modSpeed * 80 / rc
        elif rc < 100:
            pass
        else:
            modShields = modShields * 80 / rc
            modSpeed = modSpeed * 80 / rc
        
        if self.absorbedDamage > 0:
            self.absorbedDamage -= self.shiendsRegen*modShields/10
        if self.absorbedDamage < 0:
            self.absorbedDamage = 0
        self.sp = self.shields - self.absorbedDamage
        
        self.setTimeScale(modSpeed)
    
    def kill(self):
        super(Avatar, self).kill()

class Enemy(ASprite):
    def __init__(self, owner, kind, x, y):
        super(Enemy, self).__init__(kind.image)
        self.owner = owner
        self.life = kind.life
        self.damage = kind.damage
        self.score = kind.score
        self.weapons = kind.weapons
        self.settings = Settings()
        self.rays = []
        self.position = rel(x,y)
        self.target = None
        owner.enemies.append(self)
        owner.add(self, z=4)
        self.soundList = []
        self.switchBrains = kind.switchBrains
        self.do(kind.actions)
    
    def takeDamage(self, damage):
        self.life -= damage
        if self.life <= 0:
            self.owner.addExplosion(self.position)
            self.owner.score += self.score
            self.kill()
    
    def shoot(self, aim=False):
        if len(self.rays) > 0:
            laser = False
        else:
            laser = True
        for w in self.weapons:
            if w.type == PROJECTILE or w.type == TURRET:
                if aim:
                    Bullet(self, w, self.target)
                else:
                    Bullet(self, w)
            elif laser and w.type == RAY:
                self.rays.append(Ray(self, w))
            if self.settings.sound:
                if not w.startSound is None:
                    w.startSound.play()
                if not w.loopSound is None:
                    if not w.loopSound in self.soundList:
                        w.loopSound.play(-1)
                        self.soundList.append(w.loopSound)
    
    def stopShooting(self):
        for i in self.rays:
            i.kill()
        for i in self.soundList:
            i.stop()
        del self.soundList[:]
    
    def kill(self):
        if self in self.owner.enemies:
            self.owner.enemies.remove(self)
#        self.owner.cmea.remove_tricky(self)
        if self.owner.target == self:
                self.owner.target = None
        super(Enemy, self).kill()
    
    def disarm(self):
        self.weapons = tuple()

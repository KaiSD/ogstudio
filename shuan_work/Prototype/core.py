#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype core module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from cocos import menu, layer, scene, scenes, text, sprite, actions, collision_model, euclid, cocosnode
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
SPAWN = 3
AURA = 4
EFFECT = 5 

EGSIMPLE = 0
EGNOSHIELDS = 1
EGBOOSTSHIELDS = 2

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

class ActionAimMovement(actions.InstantAction):
    def __init__(self, speed, lifetime):
        super(ActionAimMovement, self).__init__()
        self.speed = speed
        self.lifetime = lifetime
    def start(self):
        actor = self.target
        target = actor.target
        angle = math.atan2(target.position[1] - actor.position[1], target.position[0] - actor.position[0])
        dy = self.speed * math.sin(angle)
        dx = self.speed * math.cos(angle)
        self.target.velocity = dx, dy
        actor.do(actions.Move() | actions.Delay(self.lifetime) +  ActionDie())

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
class DeviceKind(object):
    position = 0, 9
    damage = 2
    energy = 20
    energyIdle = 5 
    damageToShieldsMod = 1
    ammo = 0
    isGood = True
    name = "Unknown device"
    image = ""
    
    type = PROJECTILE
    # Projectile and turret params
    velocity = 0, 1600
    lifetime = 0.5
    pof = 1
    
    # Turret params
    rotation = False
    keepTarget = False
    
    # Projectile params
    directions = 0
    angle = 0
    spread = 0
    
    # Ray params
    anchor = 0, 0
    rotation = 0
    
    # Spawn params
    spawnID = ''
    
    # Effect and Aura params
    runner = None
    
    # Sound
    startSound = None
    loopSound = None
    endSound = None
    soundVolume = 0.5
    
    def __init__(self, dx=0, dy=0):
        super(DeviceKind, self).__init__()
        self.position = self.position[0] + dx, self.position[1] + dy 
        if not self.startSound is None:
            self.startSound = loadSound(self.startSound, self.soundVolume)
        if not self.endSound is None:
            self.endSound = loadSound(self.endSound, self.soundVolume)
        if not self.loopSound is None:
            self.loopSound = loadSound(self.loopSound, self.soundVolume)
        
        if self.ammo == 0:
            self.infinite = True
        else:
            self.infinite = False

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
    shields = 0
    shieldsRegen = 0
    damage = 10
    score = 1
    actions = actions.MoveBy((0,-900),duration=6) + ActionDie()
    weapons = ()

    def __init__(self):
        super(EnemyKind, self).__init__()
    
    def switchBrains(self, instance, idx):
        pass

class EffectKind(object):
    name = 'Null'
    duration = 0
    group = EGSIMPLE
    
    def start(self, instance):
        pass
    
    def effect(self, target):
        pass
    
    def check(self, target):
        return True
    
    def end(self, target):
        pass
    
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
INTERNAL KINDS
'''
class ShieldOverloadKind(EffectKind):
    name = 'Shields overloaded'
    group = EGNOSHIELDS
    
    def start(self, instance):
        target = instance.target
        instance.duration = target.shields / target.shieldsRegen
        target.playShield(-1)
    
    def effect(self, target):
        target.absorbedDamage = target.shields
    
    def end(self, instance):
        if not instance.timeToDie:
            target = instance.target
            target.absorbedDamage = 0
            target.playShield(1)

EffectShieldOverload = ShieldOverloadKind()
'''
ELEMENT CLASSES
'''
class EffectRunner(cocosnode.CocosNode):
    
    def __init__(self, kind, target, source=None):
        super(EffectRunner, self).__init__()
        self.target = target
        self.name = kind.name
        self.group = kind.group
        self.duration = kind.duration
        if source == None:
            self.source = target
        else:
            self.source = source
        kind.start(self)
        
        if self.duration == 0:
            self.constant = True
        else:
            self.constant = False
        
        self.effect = kind.effect
        self.check = kind.check
        self.end = kind.end
        target.runners.append(self)
        self.schedule_interval(self.update, 1)
        target.add(self)
        self.timeToDie = False
    
    def set_batch(self, batch, groups=None, z=0):
        pass
        
    def update(self, *args):
        if (not self.check(self)) or self.timeToDie:
            self.end(self)
            self.target.runners.remove(self)
            self.kill()
        elif not self.constant:
            self.duration -= 1
            if self.duration == 0:
                self.end(self)
                self.target.runners.remove(self)
                self.kill()

class Bullet(ASprite):
    def __init__(self, owner, kind, target=None, angle=0):
        super(Bullet, self).__init__(kind.image)
        self.position = owner.position[0] + kind.position[0], owner.position[1] + kind.position[1]
        self.damage = kind.damage
        if angle == 0:
            self.velocity = kind.velocity
        else:
            speed = kind.velocity[1]
            a = (90 - angle)/57.3
            self.velocity = speed * math.cos(a), speed * math.sin(a)
            self.rotation = angle
        self.isGood = kind.isGood
        self.needRotate = kind.rotation
        self.speed = abs(self.velocity[1])
        
        lifetime = kind.lifetime
        
        self.layer = owner.owner
        
        if self.isGood:
            self.layer.avatarBullets.append(self)
        else:
            self.layer.enemyBullets.append(self)
        
        if not target is None:
            self.aim(target)
            if kind.keepTarget:
                self.target = target
                self.schedule_interval(self.reAim, 0.1)
        
        self.layer.add(self, z=5)
        self.do(actions.Move() | actions.Delay(lifetime) +  ActionDie())
    
    def aim(self, target=None):
        speed = self.speed
        angle = math.atan2(target.position[1] - self.position[1], target.position[0] - self.position[0])
        dy = speed * math.sin(angle)
        dx = speed * math.cos(angle)
        self.velocity = dx, dy
        if self.needRotate:
            self.rotation = int(90 - angle*57.3)
    
    def reAim(self, *args):
        if self.target == None or self.target._gonnaDie:
            self.unschedule(self.reAim)
            return
        else:
            speed = self.speed
            target = self.target
            angle = math.atan2(target.position[1] - self.position[1], target.position[0] - self.position[0])
            dy = speed * math.sin(angle)
            dx = speed * math.cos(angle)
            self.velocity = dx, dy
            if self.needRotate:
                self.rotation = int(90 - angle*57.3)
    
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
        self.shieldsRegen = 0
        self.absorbedDamage = 0.0
        self.takenDamage = 0
        self.weapons = tuple()
        self.devices = kind.devices
        self._wSlots = kind.weaponSlots
        self._dSlots = kind.deviceSlots
        self.engine = kind.engine
        self.consume = 0
        self.hp = self.life
        self.sp = self.shields
        self.runners = []
        self.schedule_interval(self.regen, 0.1)
    
    def setup(self, gunsList, weaponsList, devicesList, shieldsList, enginesList, reactorList):
        settings = self.settings
        self.shields = shieldsList[settings.avatarShields][1]
        self.shieldsRegen = shieldsList[settings.avatarShields][2]
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
                  EffectRunner(EffectShieldOverload, self)
            else:
                self.playShield()
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
            self.absorbedDamage -= self.shieldsRegen*modShields/10
        if self.absorbedDamage < 0:
            self.absorbedDamage = 0
        
        for r in self.runners:
            r.effect(self)
        
        self.sp = self.shields - self.absorbedDamage
        self.setTimeScale(modSpeed)
    
    def playShield(self, idx=0):
        def die(object):
            object.kill()
        if idx == 0:
            shield = sprite.Sprite(loadAnimation('data/graphics/ShieldAvatar.png', 4, 1, 0.05))
        elif idx > 0:
            shield = sprite.Sprite(loadAnimation('data/graphics/ShieldAvatarRevived.png', 4, 1, 0.05))
        elif idx < 0:
            shield = sprite.Sprite(loadAnimation('data/graphics/ShieldAvatarBlocked.png', 4, 1, 0.05))
        self.add(shield)
        shield.do(actions.Delay(0.3) + actions.CallFuncS(die))

class Enemy(ASprite):
    def __init__(self, owner, kind, x, y, target=None):
        super(Enemy, self).__init__(kind.image)
        self.owner = owner
        self.life = kind.life
        self.shields = kind.shields
        self.shieldsRegen = kind.shieldsRegen
        self.absorbedDamage = 0.0
        self.takenDamage = 0
        self.damage = kind.damage
        self.score = kind.score
        self.weapons = kind.weapons
        self.settings = Settings()
        self.rays = []
        self.position = rel(x,y)
        self.target = target
        owner.enemies.append(self)
        owner.add(self, z=4)
        self.soundList = []
        self.switchBrains = kind.switchBrains
        self.runners = []
        self.aura = None 
        self.schedule_interval(self.regen, 1)
        self.do(kind.actions)
        self._gonnaDie = False
        self._shieldSize = kind.image.get_max_height() / 36.0
        self._auraCache = []
    
    def takeDamage(self, damage):
        if self.shields - self.absorbedDamage > 0:
            self.absorbedDamage += damage
            if self.absorbedDamage > self.shields:
                  self.takenDamage += self.absorbedDamage - self.shields
                  self.absorbedDamage = self.shields
                  EffectRunner(EffectShieldOverload, self)
            else:
                self.playShield()
        else:
            self.takenDamage += damage
        
        if self.takenDamage > self.life:
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
            elif w.type == AURA:
                self.aura = w.runner
            elif w.type == SPAWN:
                pos = abs2rel(self.position[0], self.position[1])
                Enemy(self.owner, enemies[w.spawnID], pos[0], pos[1], self.target)
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
        self.aura = None
        for i in self.soundList:
            i.stop()
        del self.soundList[:]
    
    def kill(self):
        if not self._gonnaDie:
            self._gonnaDie = True
            if self in self.owner.enemies:
                self.owner.enemies.remove(self)
#            self.owner.cmea.remove_tricky(self)
            if self.owner.target == self:
                    self.owner.target = None
            super(Enemy, self).kill()
    
    def disarm(self):
        self.weapons = tuple()
    
    def regen(self, *args):
        if self.absorbedDamage > 0:
            self.absorbedDamage -= self.shieldsRegen
        if self.absorbedDamage < 0:
            self.absorbedDamage = 0
        
        for r in self.runners:
            r.effect(self)
        
        if self.aura:
            aura = self.aura
            for e in self.owner.enemies:
                p = self.position
                ep = e.position
                if (p[0] - ep[0]) ** 2 - (p[1] - ep[1]) ** 2 <= aura.distance**2:
                    if not e in self._auraCache:
                        self._auraCache.append(e)
                        EffectRunner(aura, e, self)
                elif e in self._auraCache:
                    self._auraCache.remove(e)
                
    
    def playShield(self, idx=0):
        def die(object):
            object.kill()
        if idx == 0:
            shield = sprite.Sprite(loadAnimation('data/graphics/ShieldEnemy.png', 4, 1, 0.05))
        elif idx > 0:
            shield = sprite.Sprite(loadAnimation('data/graphics/ShieldEnemyRevived.png', 4, 1, 0.05))
        elif idx < 0:
            shield = sprite.Sprite(loadAnimation('data/graphics/ShieldEnemyBlocked.png', 4, 1, 0.05))
        shield.scale = self._shieldSize
        self.add(shield)
        shield.do(actions.Delay(0.3) + actions.CallFuncS(die))
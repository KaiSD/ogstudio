#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype core module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from cocos import menu, layer, scene, scenes, text, sprite, euclid, cocosnode
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

SLOTGUN = 0
SLOTWEAPON = 1
SLOTDEVICE = 2
SLOTNONE = 3

EGSIMPLE = 0
EGNOSHIELDS = 1
EGBOOSTSHIELDS = 2

'''
ACTION CLASSES
'''
class ActionDie(actions.InstantAction):
    def start(self):
        self.target.kill()

class ActionAim(actions.InstantAction):
    def init(self, selector=None):
        self.selector = selector
    def start(self):
        actor = self.target
        selector = self.selector
        target = None
        if selector == 'Avatar':
            target = currents['avatarObject']
        elif selector == 'AvatarTarget':
            target = currents['layerObject'].target
        elif selector == 'AnyFriend':
            target = random.choice(currents['layerObject'].avatarHelpers)
        elif selector == 'AnyEnemy':
            if currents['layerObject'].enemies:
                target = random.choice(currents['layerObject'].enemies)
        elif selector == 'Last':
            if actor._target:
                target = actor._target
        
        actor._target = target

class ActionShoot(ActionAim):
    def start(self):
        actor = self.target
        selector = self.selector
        target = None
        if selector == 'Avatar':
            target = currents['avatarObject']
        elif selector == 'AvatarTarget':
            target = currents['layerObject'].target
        elif selector == 'AnyFriend':
            target = random.choice(currents['layerObject'].avatarHelpers)
        elif selector == 'AnyEnemy':
            if currents['layerObject'].enemies:
                target = random.choice(currents['layerObject'].enemies)
        elif selector == 'Last':
            if actor._target:
                target = actor._target
            
        self.target.shoot(target)

class ActionStopShooting(actions.InstantAction):
    def start(self):
        self.target.stopShooting()

class ActionAimMovement(actions.InstantAction):
    def __init__(self, selector, speed, duration, bx1=0, by1=0, bx2=1, by2=1):
        super(ActionAimMovement, self).__init__()
        self.speed = speed
        self.duration = duration
        self.selector = selector
        self.bounds = (bx1, by1, bx2, by2)
    
    def start(self):
        actor = self.target
        
        selector = self.selector
        target = None
        if selector == 'Avatar':
            target = currents['avatarObject']
        elif selector == 'AvatarTarget':
            target = currents['layerObject'].target
        elif selector == 'AnyFriend':
            target = random.choice(currents['layerObject'].avatarHelpers)
        elif selector == 'AnyEnemy':
            if currents['layerObject'].enemies:
                target = random.choice(currents['layerObject'].enemies)
        elif selector == 'Last':
            if actor._target:
                target = actor._target
        
        if not target:
            actor.do(actions.Delay(self.duration))
            return
        
        destination = list(abs2rel(*target.position))
        if self.bounds:
            bounds = self.bounds 
            destination[0] = max(destination[0], bounds[0])
            destination[1] = max(destination[1], bounds[1])
            destination[0] = min(destination[0], bounds[2])
            destination[1] = min(destination[1], bounds[3])
        
        destination = rel(*destination)
        
        deltaY = destination[1] - actor.position[1]
        deltaX = destination[0] - actor.position[0]
        dist = math.sqrt(deltaX**2 + deltaY**2)
        if self.speed:
            dur = dist/self.speed
            coeff = self.duration/dur
        else:
            coeff = 1
        actor.do(actions.MoveBy((deltaX*coeff, deltaY*coeff), duration = self.duration))

class ActionRandomMovement(actions.IntervalAction):
    def init(self, duration, bx1=0, by1=0, bx2=1, by2=1):
        self.duration = duration
        self.initial = None
        self.destination = None
        self.bounds = (bx1, by1, bx2, by2)

    def update(self, t):
        if self.initial == None:
            self.initial = self.target.position
            destination = [random.random(), random.random()]
            if self.bounds:
                bounds = self.bounds 
                destination[0] = max(destination[0], bounds[0])
                destination[1] = max(destination[1], bounds[1])
                destination[0] = min(destination[0], bounds[2])
                destination[1] = min(destination[1], bounds[3])
            self.destination = rel(*destination)
            
        x = self.initial[0] + (self.destination[0] - self.initial[0]) * t
        y = self.initial[1] - (self.initial[1] - self.destination[1]) * t
        self.target.position = x,y

class ActionSwitchState(actions.InstantAction):
    def init(self, state):
        self.state = state
    
    def start(self):
        actor = self.target
        idx = self.state
        states = actor._kind.states
        if len(states) >= idx:
            acts = states[idx - 1]
        else:
            acte = actor.actions
        actor.stop()
        actor.actions = acts
        actor.do(acts)

class ActionSwitchWeapons(actions.InstantAction):
    def init(self, set):
        self.set = set
    
    def start(self):
        actor = self.target
        self.set = idx
        if len(actor.sets) >= idx:
            weapons = actor.set[idx - 1]
        else:
            weapons = actor.weapons
        actor.stopShooting()
        actor.weapons = weapons

class ActionMoveTo(actions.MoveTo):
    def __init__(self, x, y, duration, randomOffsetX=0, randomOffsetY=0):
        x, y = rel(x, y)
        randomOffsetX, randomOffsetY = rel(randomOffsetX, randomOffsetY)
        nx, ny = x + int((random.random() - 0.5)*randomOffsetX),  y + int((random.random() - 0.5)*randomOffsetY), 
        super(ActionMoveTo, self).__init__((nx, -ny), duration=duration)

class ActionMoveBy(actions.MoveBy):
    def __init__(self, x, y, duration, randomOffsetX=0, randomOffsetY=0):
        x, y = rel(x, y)
        randomOffsetX, randomOffsetY = rel(randomOffsetX, randomOffsetY)
        nx, ny = x + int((random.random() - 0.5)*randomOffsetX),  y + int((random.random() - 0.5)*randomOffsetY),
        super(ActionMoveBy, self).__init__((nx, ny), duration=duration)

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
LIBRARY ENTRIES
'''
adata['aDie'] = ActionDie()
adata['aShoot'] = ActionShoot()
adata['aAimShoot'] = ActionShoot('Avatar')
adata['aStopShooting'] = ActionStopShooting()
adata['aAimMove400'] = ActionAimMovement('Avatar', 400, 3)
adata['aAimMove100'] = ActionAimMovement('Avatar', 100, 9)

adata['aRandMove5'] = ActionRandomMovement(duration=5)
adata['aRandMove4'] = ActionRandomMovement(duration=4)
adata['aRandMove3'] = ActionRandomMovement(duration=3) 

'''
MAIN KINDS
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
    oneByOne = False
    
    # Ray params
    anchor = 0, 0
    
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
        
        if self.oneByOne:
            self.tick = 0
        self.amod = 1

class AvatarKind(object):
    image = loadAnimation('data/graphics/avatarShip.png', 3, 1, 0.1, True)
    life = 100
    engine = 1
    weapons = ()
    weaponSlots = ()
    deviceSlots = (1, 2, 3)
    name = 'Avatar'
    
    def __init__(self):
        super(AvatarKind, self).__init__()

class NPCKind(object):
    image = loadAnimation('data/graphics/enemy1.png', 2, 1, 0.5, True)
    life = 10
    shields = 0
    shieldsRegen = 0
    damage = 10
    score = 1
    brains = tuple()
    sets = tuple()
    weapons = tuple()
    
    def __init__(self):
        super(NPCKind, self).__init__()
        
        states = []
        for i in self.brains:
            l = loadScript(i)
            blocks = [[]]
            for j in l:
                if j[0] == 'New':
                    if blocks[-1]:
                        blocks.append([j])
                elif j[0] == 'Repeat':
                    if blocks[-1]:
                        if blocks[-1][-1][0] == 'New':
                            blocks[-1].append(j)
                        else:
                            blocks.append([j])
                    else:
                        blocks[-1].append(j)
                else:
                    blocks[-1].append(j)
            states.append(self.translate(blocks))
        self.states = states
        
        if states:
            if states[0]:
                self.actions = states[0]
    
    def translate(self, blocks):
        commands = {
                    'SelectTarget': ActionAim,
                    'AimMove': ActionAimMovement,
                    'Wait': actions.Delay,
                    'Die': ActionDie,
                    'MoveBy': ActionMoveBy,
                    'MoveTo': ActionMoveTo,
                    'RandomDelay': actions.RandomDelay,
                    'RandomMovement': ActionRandomMovement,
                    'Shoot': ActionShoot,
                    'StopShooting': ActionStopShooting,
                    'SwitchStates': ActionSwitchState,
                    'SwitchWeapons': ActionSwitchWeapons,
                    }
        
        isLoop = False
        isNew = False 
        acts = None
        
        for block in blocks:
            if block[0][0] == 'New':
                isNew = True
                del block[0]
            else:
                isNew = False
            if block:
                if block[0][0] == 'Repeat':
                    isLoop = True
                    del block[0]
                else:
                    isLoop = False
                
                if block:
                    cmd = block[0]
                    current_acts = commands[cmd[0]](*cmd[1:])
                    del block[0]
                    
                    for cmd in block:
                        current_acts += commands[cmd[0]](*cmd[1:])
                
                    if isLoop:
                        current_acts = actions.Repeat(current_acts)
                    
                    if acts and not isNew:
                        acts += current_acts
                    if acts and isNew:
                        acts = acts | current_acts
                    else:
                        acts = current_acts
        return acts
            
        

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
EFFECTS
'''
class RechargerKind(EffectKind):
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
            target.absorbedDamage = target.shields * 3 / 4
            target.playShield(1)

class DefenderKind(EffectKind):
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

effectsData['eOverload'] = ShieldOverloadKind()
effectsData['eRecharge'] = RechargerKind()
effectsData['eDefend'] = DefenderKind()

'''
MAIN GAME ELEMENTS
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
        l = self.target.runners
        if (not self.check(self)) or self.timeToDie:
            self.end(self)
            if self in l:
                l.remove(self)
            self.kill()
        elif not self.constant:
            self.duration -= 1
            if self.duration == 0:
                self.end(self)
                if self in l:
                    l.remove(self)
                self.kill()

class Bullet(ASprite):
    def __init__(self, owner, kind, target=None, angle=0):
        super(Bullet, self).__init__(kind.image)
        self.position = owner.position[0] + kind.position[0], owner.position[1] + kind.position[1]
        self.damage = kind.damage
        if angle == 0:
            self.velocity = kind.velocity
            self.rotation = 0
        else:
            speed = kind.velocity[1]
            a = (90 - angle)/57.3
            self.velocity = speed * math.cos(a), speed * math.sin(a)
            self.rotation = angle
        self.isGood = kind.isGood
        self._needRotate = kind.rotation
        self._kind = kind
        self._speed = kind.velocity[1]

        lifetime = kind.lifetime
        
        if self.isGood:
            currents['layerObject'].avatarBullets.append(self)
        else:
            currents['layerObject'].enemyBullets.append(self)
        
        if not target is None:
            self.aim(target)
            if kind.keepTarget:
                self.target = target
                self.schedule_interval(self.reAim, 0.1)
        
        used = bulletsUsed.get(kind, [])
        used.append(self)
        bulletsUsed[kind] = used
        
        currents['layerObject'].add(self, z=5)
        self._actions = adata['aMove'] | actions.Delay(lifetime) + adata['aDie']
        self.do(self._actions)
    
    def aim(self, target=None):
        speed = abs(self._kind.velocity[1])
        angle = math.atan2(target.position[1] - self.position[1], target.position[0] - self.position[0])
        dy = speed * math.sin(angle)
        dx = speed * math.cos(angle)
        self.velocity = dx, dy
        if self._needRotate:
            self.rotation = int(90 - angle*57.3)
    
    def reAim(self, *args):
        if self.target == None or self.target._gonnaDie:
            self.unschedule(self.reAim)
            return
        else:
            speed = self._speed
            target = self.target
            angle = math.atan2(target.position[1] - self.position[1], target.position[0] - self.position[0])
            dy = speed * math.sin(angle)
            dx = speed * math.cos(angle)
            self.velocity = dx, dy
            if self._needRotate:
                self.rotation = int(90 - angle*57.3)
    
    def kill(self):
        if self.isGood:
            currents['layerObject'].avatarBullets.remove(self)
        else:
            currents['layerObject'].enemyBullets.remove(self)
        if self._kind.keepTarget:
            self.unschedule(self.reAim)
        
        kind = self._kind
        bulletsUsed[kind].remove(self)
        free = bulletsFree.get(kind, [])
        free.append(self)
        bulletsFree[kind] = free
        currents['layerObject'].remove(self)
        self.stop()
    
    def reinstate(self, owner, target=None, angle=0):
        kind = self._kind
        self.position = owner.position[0] + kind.position[0], owner.position[1] + kind.position[1]
        if angle == 0:
            self.velocity = kind.velocity
            self.rotation = 0
        else:
            speed = kind.velocity[1]
            a = (90 - angle)/57.3
            self.velocity = speed * math.cos(a), speed * math.sin(a)
            self.rotation = angle
        
        if self.isGood:
            currents['layerObject'].avatarBullets.append(self)
        else:
            currents['layerObject'].enemyBullets.append(self)
        
        if not target is None:
            self.aim(target)
            if kind.keepTarget:
                self.target = target
                self.schedule_interval(self.reAim, 0.1)
        
        bulletsFree[kind].remove(self)
        bulletsUsed[kind].append(self)
        
        currents['layerObject'].add(self, z=5)
        self.do(self._actions)

class Ray(ASprite):
    def __init__(self, owner, kind):
        super(Ray, self).__init__(kind.image)
        self.image_anchor = kind.anchor
        self.rotation = kind.rayRotation
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
        self.devices = tuple()
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
            weapons[-1].amod = -1
            self.consume += gunsList[settings.avatarGun].energyIdle
        for i in self.settings.avatarWeapons:
            if len(weapons) < len(self._wSlots):
                weapons.append(weaponsList[i](self._wSlots[len(weapons)]))
                self.consume += weaponsList[i].energyIdle
        self.weapons = tuple(weapons)
        devices = []
        for i in self.settings.avatarDevices:
            if len(devices) < len(self._dSlots):
                devices.append(devicesList[i](self._dSlots[len(devices)]))
                self.consume += devicesList[i].energyIdle
        self.devices = tuple(devices)
        
    
    def takeDamage(self, damage, damageToShieldsMod=1):
        if self.shields - self.absorbedDamage > 0:
            self.absorbedDamage += damage
            if self.absorbedDamage > self.shields:
                  self.takenDamage += self.absorbedDamage - self.shields
                  self.absorbedDamage = self.shields
                  EffectRunner(effectsData['eOverload'], self)
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
        shield.do(adata['aDelay03'] + actions.CallFuncS(die))

class NPCShip(ASprite):
    def __init__(self, owner, kind, x, y, coordZ=4):
        super(NPCShip, self).__init__(kind.image)
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
        self.soundList = []
        self.runners = []
        self.aura = None 
        self._gonnaDie = False
        self._shieldSize = kind.image.get_max_height() / 36.0
        self._auraCache = []
        self._kind =  kind
        self._target = None
        self.velocity = 0, 0
        used = shipsUsed.get(kind, [])
        used.append(self)
        shipsUsed[kind] = used
        self.schedule_interval(self.regen, 1)
        self.do(kind.actions)
        owner.add(self, z=coordZ)
    
    def takeDamage(self, damage):
        if self.shields - self.absorbedDamage > 0:
            self.absorbedDamage += damage
            if self.absorbedDamage > self.shields:
                  self.takenDamage += self.absorbedDamage - self.shields
                  self.absorbedDamage = self.shields
                  EffectRunner(effectsData['eOverload'], self)
            else:
                self.playShield()
        else:
            self.takenDamage += damage
        
        if self.takenDamage > self.life:
            self.owner.addExplosion(self.position)
            self.owner.score += self.score
            self.kill()
            
    
    def shoot(self, target=None):
        if len(self.rays) > 0:
            laser = False
        else:
            laser = True
        for w in self.weapons:
            if w.type == PROJECTILE or w.type == TURRET:
                free = bulletsFree.get(w, []) 
                if target:
                    if free:
                        free[0].reinstate(self, target)
                    else:
                        Bullet(self, w, target)
                else:
                    if free:
                        free[0].reinstate(self)
                    else:
                        Bullet(self, w)
            elif laser and w.type == RAY:
                self.rays.append(Ray(self, w))
            elif w.type == AURA:
                self.aura = w.runner
            elif w.type == SPAWN:
                pos = abs2rel(*self.position)
                Enemy(self.owner, enemies[w.spawnID], pos[0], pos[1])
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
            layer = currents['layerObject']
            self._gonnaDie = True
            if self.good:
                layer.avatarHelpers.remove(self)
            else:
                layer.enemies.remove(self)
            if self.owner.target == self:
                    self.owner.target = None
            kind = self._kind
            shipsUsed[kind].remove(self)
            free = shipsFree.get(kind, [])
            free.append(self)
            shipsFree[kind] = free
            self.unschedule(self.regen)
            layer.remove(self)
            self.stop()
    
    def reinstate(self, x, y, target=None, coordZ=4):
        layer = currents['layerObject']
        kind = self._kind
        self.absorbedDamage = 0.0
        self.takenDamage = 0
        self.weapons = kind.weapons
        self.settings = Settings()
        self.rays = []
        self.position = rel(x,y)
        self.target = target
        self.soundList = []
        self.runners = []
        self.aura = None 
        self.schedule_interval(self.regen, 1)
        self.do(kind.actions)
        self._gonnaDie = False
        self._auraCache = []
        self.velocity = 0, 0
        layer.add(self, z=coordZ)
        if self.good:
            layer.avatarHelpers.append(self)
        else:
            layer.enemies.append(self)
        
        shipsFree[kind].remove(self)
        shipsUsed[kind].append(self)
        
        layer.add(self, z=5)
    
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
            for e in currents['layerObject'].enemies:
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
        shield.do(adata['aDelay03'] + actions.CallFuncS(die))

class Enemy(NPCShip):
    def __init__(self, owner, kind, x, y):
        super(Enemy, self).__init__(owner, kind, x, y)
        owner.enemies.append(self)
        self.good = False

class Helper(NPCShip):
    def __init__(self, owner, kind, x, y, target=None):
        super(Helper, self).__init__(owner, kind, x, y, 8)
        owner.avatarHelpers.append(self)
        self.good = True
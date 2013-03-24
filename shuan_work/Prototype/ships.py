#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype core module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from devices import *

'''
AVATARS
'''
class AvatarMK1(AvatarKind):
    image = loadAnimation('data/graphics/avatarSmallShip.png', 3, 1, 0.1, True)
    life = 100
    engine = 1
    name = "Avatar MK1"
    
    weaponSlots = (-5, 5, 0)
    
    def __init__(self):
        super(AvatarKind, self).__init__()

class AvatarMK2(AvatarKind):
    image = loadAnimation('data/graphics/avatarSmallShip.png', 3, 1, 0.1, True)
    life = 125
    engine = 1
    name = "Avatar MK2"
    
    weaponSlots = (-5, 5, -13, 13)
    
    def __init__(self):
        super(AvatarKind, self).__init__()

class AvatarMK3(AvatarKind):
    image = loadAnimation('data/graphics/avatarSmallShip.png', 3, 1, 0.1, True)
    life = 150
    engine = 1
    name = "Avatar MK3"
    
    weaponSlots = (-5, 5, 0, -13, 13)
    
    def __init__(self):
        super(AvatarKind, self).__init__()
'''
HELPERS
'''
class HelperAimer(NPCKind):
    """
    Добрая тарелка
    """
    image = loadAnimation('data/graphics/helper0.png', 3, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    weapons = (HelperGun(),)
    actions = actions.Repeat(ActionFollowAvatar(speed=200, duration=0.5)) | actions.Repeat(actionDelay1 + actionAimAndShootInst)
'''
ENEMIES
'''
class EnemyDummy(NPCKind):
    """
    Бочка
    """
    image = loadAnimation('data/graphics/enemy0.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    actions = actions.MoveTo((int(random.random()*800),-900),duration=9) + actionDieInst

class EnemyMine(NPCKind):
    """
    Мина
    """
    image = loadAnimation('data/graphics/enemyMine.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 0
    actions = actions.MoveBy((0,60),duration=1) + ActionAimMovement(100, 9)

class EnemyDumbMine(NPCKind):
    """
    Глупая Мина
    """
    image = loadAnimation('data/graphics/enemyMine.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 0
    actions = actions.MoveBy((0,60),duration=1) + actionMove900D9 + actionDieInst

class EnemyAimer(NPCKind):
    """
    Тарелка
    """
    image = loadAnimation('data/graphics/enemy1.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    weapons = (EnemyGun(),)
    actions = actionMove900D6 + actionDieInst | actions.Repeat(actions.RandomDelay(1, 3) + actionAimAndShootInst)

class EnemyStraighter(NPCKind):
    """
    Мясо
    """
    image = loadAnimation('data/graphics/enemy2.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    weapons = (EnemyGun(),)
    actions = actions.MoveTo((int(random.random()*800),-900),duration=6) + actionDieInst | actions.Repeat(actions.RandomDelay(0.5, 2) + actionShootInst)

class EnemyKami(NPCKind):
    """
    Камикадзе
    """
    image = loadAnimation('data/graphics/enemy5.png', 2, 1, 0.5, True)
    life = 20
    damage = 20
    score = 1
    actions = actions.MoveBy((0,-100),duration=1) + ActionAimMovement(400, 3)

class EnemyRayer(NPCKind):
    """
    Фонарь
    """
    image = loadAnimation('data/graphics/enemy3.png', 2, 1, 0.5, True)
    life = 30
    damage = 20
    score = 3
    weapons = (EnemyLaser(),)
    actions = actions.MoveTo((int(random.random()*800),-900),duration=10) + actionDieInst | actions.Repeat(actions.RandomDelay(0.5, 2) + actionShootInst + actions.RandomDelay(2, 4) + actionStopShootingInst)

class EnemyBurster(NPCKind):
    """
    Спаммер
    """
    image = loadAnimation('data/graphics/enemy4.png', 3, 1, 0.1, True)
    life = 20
    damage = 10
    score = 2
    weapons = (EnemyGun(),)
    actions = actions.MoveTo((int(random.random()*800),-900),duration=12) + actionDieInst | actions.Repeat(actions.Delay(0.5) + actionShootInst)

class EnemyBuffer(NPCKind):
    """
    Болельщица
    """
    image = loadAnimation('data/graphics/enemy7.png', 2, 1, 0.5, True)
    life = 20
    damage = 20
    shields = 20
    shieldsRegen = 1
    score = 5
    weapons = (EnemyShieldProjector(),)
    actions = actionRandomMovementD5 + actionRandomMovementD5 + actionRandomMovementD5 + actionMove900D5 + actionDieInst | actionShootInst

class EnemyBehemoth(NPCKind):
    """
    Бегемот
    """
    image = loadAnimation('data/graphics/enemy6.png', 2, 1, 0.1, True)
    life = 100
    damage = 50
    score = 5
    weapons = (EnemyGun(-15,-30), EnemyGun(0,-30), EnemyGun(15,-30))
    actions = actionRandomMovementD3 + actionRandomMovementD3 + actionRandomMovementD3 + actionMove900D6 + actionDieInst | actions.Repeat(actions.RandomDelay(0.5, 2) + actionAimAndShootInst) | actions.Repeat(actions.Delay(0.5) + actionShootInst)

class EnemySummoner(NPCKind):
    """
    Нянька
    """
    image = loadAnimation('data/graphics/enemy8.png', 2, 1, 0.1, True)
    life = 100
    damage = 50
    score = 5
    weapons = (EnemySpawnAimer(), EnemyGun(-15,-30), EnemyGun(15,-30))
    actions = actionRandomMovementD5 + actionRandomMovementD5 + actionRandomMovementD5 + actionMove900D5 + actionDieInst | actions.Repeat(actions.Delay(3) + actionShootInst)

class EnemyMinador(NPCKind):
    """
    Минадор
    """
    image = loadAnimation('data/graphics/enemy9.png', 2, 1, 0.1, True)
    life = 100
    damage = 50
    score = 5
    weapons = (EnemySpawnMine(), )
    actions = actionRandomMovementD5 + actionRandomMovementD5 + actionRandomMovementD5 + actionMove900D5 + actionDieInst | actions.Repeat(actions.Delay(2) + actionShootInst)

class EnemyMiniBoss(NPCKind):
    """
    Тестовый минибосс
    """
    image = loadAnimation('data/graphics/miniboss.png', 1, 1, 0.1, True)
    life = 1000
    damage = 1000
    score = 100
    weapons = (EnemyGun(-15,-30), EnemyGun(15,-30))
    actions =  actions.Repeat(actionRandomMovementD4) | actions.Repeat(actions.Delay(0.2) + actionAimAndShootInst)

class EnemyTestBoss(NPCKind):
    """
    Тестовый босс
    """
    image = loadAnimation('data/graphics/boss.png', 1, 1, 0.1, True)
    life = 3000
    damage = 1000
    score = 300
    weapons = (EnemyGun(-15,-30), EnemyGun(15,-30), EnemyGun(-40,-35), EnemyGun(40,-35))
    weapons2 = (EnemyGun(-15,-30), EnemyGun(15,-30), EnemyGun(-40,-35), EnemyGun(40,-35), EnemyLaser())
    actions =  actions.Repeat(actionRandomMovementD4) | actions.Repeat(actions.Delay(0.4) + actionAimAndShootInst)
    
    def switchBrains(self, instance, idx):
        if idx == 0:
            instance.weapons = EnemyTestBoss.weapons
            newActions = EnemyTestBoss.actions
        elif idx == 1:
            instance.weapons = EnemyTestBoss.weapons2
            newActions = actions.MoveTo((instance.target.position[0], relY(0.1)), duration=1) + actions.Repeat(ActionRandomMovement(duration=8)) | actions.Repeat(actions.Delay(0.5) + actionAimAndShootInst) | actions.Repeat(actions.Delay(2) + actionStopShootingInst)
        elif idx == 2:
            instance.weapons = EnemyTestBoss.weapons2
            newActions = actions.MoveTo((instance.target.position[0], relY(0.1)), duration=1) + actions.Repeat(actionRandomMovementD4) | actions.Repeat(actions.Delay(0.2) + actionAimAndShootInst)    
        instance.stop()
        instance.do(actionStopShootingInst + newActions)

class ShipKindLoader(NPCKind):
    """
    Загрузчик кайндов кораблей
    """
    def __init__(self, filename):
        data = jsonLoad(filename)
        

enemies['Dummy'] = EnemyDummy()
enemies['Mine'] = EnemyMine()
enemies['DumbMine'] = EnemyDumbMine()
enemies['Aimer'] = EnemyAimer()
enemies['Straighter'] = EnemyStraighter()
enemies['Kami'] = EnemyKami()
enemies['Burster'] = EnemyBurster()
enemies['Rayer'] = EnemyRayer()
enemies['Buffer'] = EnemyBuffer()
enemies['Minador'] = EnemyMinador()
enemies['Behemoth'] = EnemyBehemoth()
enemies['Summoner'] = EnemySummoner()

enemies['Miniboss'] = EnemyMiniBoss()
enemies['TestBoss'] = EnemyTestBoss()

helpers['Aimer'] = HelperAimer()

playerShips += (AvatarMK1, AvatarMK2, AvatarMK3)
playerGuns += (Empty, Minigun)
playerWeapons += (Empty, Laser, Turret)
playerDevices += (Empty, Recharger, RocketLauncher, Swarm, Satelite)
playerShields += (('No Shield',0,0,0), ('Shield MK1',10,1,0))
playerEngines += (('Engine MK1',5.0,12), ('Engine MK2', 10.0,50))
playerReactors += (('Reactor MK1',100), ('Reactor MK2', 150))
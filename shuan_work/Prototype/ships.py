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
    weapons = (helperWeapons['HelperGun'](),)
    brains = ['data/brains/satelite.seq'] 
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
    brains = ['data/brains/dummy.seq']

class EnemyMine(NPCKind):
    """
    Мина
    """
    image = loadAnimation('data/graphics/enemyMine.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 0
    brains = ['data/brains/smartmine.seq']

class EnemyDumbMine(NPCKind):
    """
    Глупая Мина
    """
    image = loadAnimation('data/graphics/enemyMine.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 0
    brains = ['data/brains/dumbmine.seq']

class EnemyAimer(NPCKind):
    """
    Тарелка
    """
    image = loadAnimation('data/graphics/enemy1.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    weapons = (enemyWeapons['EnemyGun'](),)
    brains = ['data/brains/aimer.seq']

class EnemyStraighter(NPCKind):
    """
    Мясо
    """
    image = loadAnimation('data/graphics/enemy2.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    weapons = (enemyWeapons['EnemyGun'](),)
    brains = ['data/brains/straighter.seq']

class EnemyKami(NPCKind):
    """
    Камикадзе
    """
    image = loadAnimation('data/graphics/enemy5.png', 2, 1, 0.5, True)
    life = 20
    damage = 20
    score = 1
    brains = ['data/brains/kami.seq']

class EnemyRayer(NPCKind):
    """
    Фонарь
    """
    image = loadAnimation('data/graphics/enemy3.png', 2, 1, 0.5, True)
    life = 30
    damage = 20
    score = 3
    weapons = (enemyWeapons['EnemyLaser'](),)
    brains = ['data/brains/rayer.seq']

class EnemyBurster(NPCKind):
    """
    Спаммер
    """
    image = loadAnimation('data/graphics/enemy4.png', 3, 1, 0.1, True)
    life = 20
    damage = 10
    score = 2
    weapons = (enemyWeapons['EnemyGun'](),)
    brains = ['data/brains/burster.seq']

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
    weapons = (enemyWeapons['EnemyShieldProjector'](),)
    brains = ['data/brains/buffer.seq']

class EnemyBehemoth(NPCKind):
    """
    Бегемот
    """
    image = loadAnimation('data/graphics/enemy6.png', 2, 1, 0.1, True)
    life = 100
    damage = 50
    score = 5
    weapons = (enemyWeapons['EnemyGun'](-15,-30), enemyWeapons['EnemyGun'](0,-30), enemyWeapons['EnemyGun'](15,-30))
    actions = adata['aRandMove3'] + adata['aRandMove3'] + adata['aRandMove3'] + adata['aDown6'] + adata['aDie'] | actions.Repeat(actions.RandomDelay(0.5, 2) + adata['aAimShoot']) | actions.Repeat(actions.Delay(0.5) + adata['aShoot'])

class EnemySummoner(NPCKind):
    """
    Нянька
    """
    image = loadAnimation('data/graphics/enemy8.png', 2, 1, 0.1, True)
    life = 100
    damage = 50
    score = 5
    weapons = (enemyWeapons['EnemyGun'](), enemyWeapons['EnemyGun'](-15,-30), enemyWeapons['EnemyGun'](15,-30))
    actions = adata['aRandMove5'] + adata['aRandMove5'] + adata['aRandMove5'] + adata['aDown5'] + adata['aDie'] | actions.Repeat(actions.Delay(3) + adata['aShoot'])

class EnemyMinador(NPCKind):
    """
    Минадор
    """
    image = loadAnimation('data/graphics/enemy9.png', 2, 1, 0.1, True)
    life = 100
    damage = 50
    score = 5
    weapons = (enemyWeapons['EnemySpawnMine'](), )
    actions = adata['aRandMove5'] + adata['aRandMove5'] + adata['aRandMove5'] + adata['aDown5'] + adata['aDie'] | actions.Repeat(actions.Delay(2) + adata['aShoot'])

class EnemyMiniBoss(NPCKind):
    """
    Тестовый минибосс
    """
    image = loadAnimation('data/graphics/miniboss.png', 1, 1, 0.1, True)
    life = 1000
    damage = 1000
    score = 100
    weapons = (enemyWeapons['EnemyGun'](-15,-30), enemyWeapons['EnemyGun'](15,-30))
    actions =  actions.Repeat(adata['aRandMove4']) | actions.Repeat(actions.Delay(0.2) + adata['aAimShoot'])

class EnemyTestBoss(NPCKind):
    """
    Тестовый босс
    """
    image = loadAnimation('data/graphics/boss.png', 1, 1, 0.1, True)
    life = 3000
    damage = 1000
    score = 300
    weapons = (enemyWeapons['EnemyGun'](-15,-30), enemyWeapons['EnemyGun'](15,-30), enemyWeapons['EnemyGun'](-40,-35), enemyWeapons['EnemyGun'](40,-35))
    weapons2 = (enemyWeapons['EnemyGun'](-15,-30), enemyWeapons['EnemyGun'](15,-30), enemyWeapons['EnemyGun'](-40,-35), enemyWeapons['EnemyGun'](40,-35), enemyWeapons['EnemyLaser']())
    actions =  actions.Repeat(adata['aRandMove4']) | actions.Repeat(actions.Delay(0.4) + adata['aAimShoot'])
    
    def switchBrains(self, instance, idx):
        if idx == 0:
            instance.weapons = EnemyTestBoss.weapons
            newActions = EnemyTestBoss.actions
        elif idx == 1:
            instance.weapons = EnemyTestBoss.weapons2
            newActions = actions.MoveTo((instance.target.position[0], relY(0.1)), duration=1) + actions.Repeat(ActionRandomMovement(duration=8)) | actions.Repeat(actions.Delay(0.5) + adata['aAimShoot']) | actions.Repeat(actions.Delay(2) + adata['aStopShooting'])
        elif idx == 2:
            instance.weapons = EnemyTestBoss.weapons2
            newActions = actions.MoveTo((instance.target.position[0], relY(0.1)), duration=1) + actions.Repeat(adata['aRandMove4']) | actions.Repeat(actions.Delay(0.2) + adata['aAimShoot'])    
        instance.stop()
        instance.do(adata['aStopShooting'] + newActions)

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
playerShields += (('No Shield',0,0,0), ('Shield MK1',10,1,0))
playerEngines += (('Engine MK1',5.0,12), ('Engine MK2', 10.0,50))
playerReactors += (('Reactor MK1',100), ('Reactor MK2', 150))
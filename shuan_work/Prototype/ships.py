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
    image = loadAnimation('data/graphics/avatarShip.png', 3, 1, 0.1, True)
    life = 100
    engine = 1
    name = "Avatar MK1"
    
    weaponSlots = (-5, 7, 0)
    
    def __init__(self):
        super(AvatarKind, self).__init__()

class AvatarMK2(AvatarKind):
    image = loadAnimation('data/graphics/avatarShip.png', 3, 1, 0.1, True)
    life = 125
    engine = 1
    name = "Avatar MK2"
    
    weaponSlots = (-5, 7, -13, 13)
    
    def __init__(self):
        super(AvatarKind, self).__init__()

class AvatarMK3(AvatarKind):
    image = loadAnimation('data/graphics/avatarShip.png', 3, 1, 0.1, True)
    life = 150
    engine = 1
    name = "Avatar MK3"
    
    weaponSlots = (-5, 7, 0, -13, 13)
    
    def __init__(self):
        super(AvatarKind, self).__init__()

'''
ENEMIES
'''
class EnemyDummy(EnemyKind):
    """
    Бочка
    """
    image = loadAnimation('data/graphics/enemy0.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    actions = actions.MoveTo((int(random.random()*800),-900),duration=9) + ActionDie()
class EnemyAimer(EnemyKind):
    """
    Тарелка
    """
    image = loadAnimation('data/graphics/enemy1.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    weapons = (EnemyGun(),)
    actions = actions.MoveBy((0,-900),duration=6) + ActionDie() | actions.Repeat(actions.RandomDelay(1, 3) + ActionAimAndShoot())
class EnemyStraighter(EnemyKind):
    """
    Мясо
    """
    image = loadAnimation('data/graphics/enemy2.png', 2, 1, 0.5, True)
    life = 10
    damage = 10
    score = 1
    weapons = (EnemyGun(),)
    actions = actions.MoveTo((int(random.random()*800),-900),duration=6) + ActionDie() | actions.Repeat(actions.RandomDelay(0.5, 2) + ActionShoot())
class EnemyKami(EnemyKind):
    """
    Камикадзе
    """
    image = loadAnimation('data/graphics/enemy5.png', 2, 1, 0.5, True)
    life = 20
    damage = 20
    score = 1
    actions = actions.MoveBy((0,-100),duration=1) + ActionAimMovement(400, 3)
class EnemyRayer(EnemyKind):
    """
    Фонарь
    """
    image = loadAnimation('data/graphics/enemy3.png', 2, 1, 0.5, True)
    life = 30
    damage = 20
    score = 3
    weapons = (EnemyLaser(),)
    actions = actions.MoveTo((int(random.random()*800),-900),duration=10) + ActionDie() | actions.Repeat(actions.RandomDelay(0.5, 2) + ActionShoot() + actions.RandomDelay(2, 4) + ActionStopShooting())
class EnemyBurster(EnemyKind):
    """
    Спаммер
    """
    image = loadAnimation('data/graphics/enemy4.png', 3, 1, 0.1, True)
    life = 20
    damage = 10
    score = 2
    weapons = (EnemyGun(),)
    actions = actions.MoveTo((int(random.random()*800),-900),duration=12) + ActionDie() | actions.Repeat(actions.Delay(0.5) + ActionShoot())

class EnemyBehemoth(EnemyKind):
    """
    Бегемот
    """
    image = loadAnimation('data/graphics/enemy6.png', 2, 1, 0.1, True)
    life = 100
    damage = 50
    score = 5
    weapons = (EnemyGun(-15,-30), EnemyGun(15,-30))
    actions = ActionRandomMovement(duration=3) + ActionRandomMovement(duration=3) + ActionRandomMovement(duration=3) + actions.MoveBy((0,-900),duration=6) + ActionDie() | actions.Repeat(actions.RandomDelay(0.5, 2) + ActionAimAndShoot()) | actions.Repeat(actions.Delay(0.5) + ActionShoot())

class EnemySummoner(EnemyKind):
    """
    Нянька
    """
    image = loadAnimation('data/graphics/enemy6.png', 2, 1, 0.1, True)
    life = 100
    damage = 50
    score = 5
    weapons = (EnemySpawnAimer(), )
    actions = ActionRandomMovement(duration=5) + ActionRandomMovement(duration=5) + ActionRandomMovement(duration=5) + actions.MoveBy((0,-900),duration=5) + ActionDie() | actions.Repeat(actions.Delay(3) + ActionShoot())

class EnemyMiniBoss(EnemyKind):
    """
    Тестовый минибосс
    """
    image = 'data/graphics/miniboss.png'
    life = 1000
    damage = 1000
    score = 100
    weapons = (EnemyGun(-15,-30), EnemyGun(15,-30))
    actions =  actions.Repeat(ActionRandomMovement(duration=4)) | actions.Repeat(actions.Delay(0.2) + ActionAimAndShoot())

class EnemyTestBoss(EnemyKind):
    """
    Тестовый босс
    """
    image = 'data/graphics/boss.png'
    life = 3000
    damage = 1000
    score = 300
    weapons = (EnemyGun(-15,-30), EnemyGun(15,-30), EnemyGun(-40,-35), EnemyGun(40,-35))
    weapons2 = (EnemyGun(-15,-30), EnemyGun(15,-30), EnemyGun(-40,-35), EnemyGun(40,-35), EnemyLaser())
    actions =  actions.Repeat(ActionRandomMovement(duration=4)) | actions.Repeat(actions.Delay(0.4) + ActionAimAndShoot())
    
    def switchBrains(self, instance, idx):
        if idx == 0:
            instance.weapons = EnemyLastBoss.weapons
            newActions = EnemyLastBoss.actions
        elif idx == 1:
            instance.weapons = EnemyLastBoss.weapons2
            newActions = actions.MoveTo((instance.target.position[0], relY(0.1)), duration=1) + actions.Repeat(ActionRandomMovement(duration=8)) | actions.Repeat(actions.Delay(0.5) + ActionAimAndShoot()) | actions.Repeat(actions.Delay(2) + ActionStopShooting())
        elif idx == 2:
            instance.weapons = EnemyLastBoss.weapons2
            newActions = actions.MoveTo((instance.target.position[0], relY(0.1)), duration=1) + actions.Repeat(ActionRandomMovement(duration=4)) | actions.Repeat(actions.Delay(0.2) + ActionAimAndShoot())    
        instance.stop()
        instance.do(ActionStopShooting() + newActions)

enemies['Dummy'] = EnemyDummy()
enemies['Aimer'] = EnemyAimer()
enemies['Straighter'] = EnemyStraighter()
enemies['Kami'] = EnemyKami()
enemies['Burster'] = EnemyBurster()
enemies['Rayer'] = EnemyRayer()
enemies['Behemoth'] = EnemyBehemoth()
enemies['Summoner'] = EnemySummoner()
enemies['Miniboss'] = EnemyMiniBoss()
enemies['TestBoss'] = EnemyTestBoss()

playerShips += (AvatarMK1, AvatarMK2, AvatarMK3)
playerGuns += (Empty, Minigun, )
playerWeapons += (Empty, Laser, Turret)
playerDevices += tuple()
playerShields += (('No Shield',0,0,0), ('Shield MK1',10,1,0))
playerEngines += (('Engine MK1',5.0,12), ('Engine MK2', 10.0,50))
playerReactors += (('Reactor MK1',100), ('Reactor MK2', 150))
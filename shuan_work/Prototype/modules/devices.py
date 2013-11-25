#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype core module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from core import *
from loadcsv import LoadCSV

'''
BASIC DEVICE
'''
class Empty(DeviceKind):
    type = EMPTY
    name = "None"
    energy = 0
    energyIdle = 0

def loadDeviceKind(data):
    get = data.get
    
    imgFile = get('image', '')
    aniInfo = get('animationInfo', [])
    if aniInfo:
        img = loadAnimation(imgFile, *aniInfo)
    else:
        img = str(imgFile)
            
    class LoadedDeviceKind(DeviceKind):
        position = get('position', (0, 9))
        damage = get('damage', 2) 
        energy = get('energy', 20)
        energyIdle = get('energyIdle', 5) 
        damageToShieldMod = get('damageToShieldMod', 1)
        ammo = get('ammo', 0)
        isGood = get('isGood', True)
        name = get('name', "Unknown device")
        image = img
        type = ('EMPTY', 'PROJECTILE', 'RAY', 'TURRET', 'SPAWN', 'AURA', 'EFFECT').index(get('type', 'PROJECTILE')) - 1
        velocity = (0, get('velocity', (0, 1600)))
        lifetime = get('lifetime', 0.5)
        pof = get('pof', 1)
        bulletRotation = get('bulletRotation', False)
        rayRotation = get('rayRotation', False)
        keepTarget = get('keepTarget', False)
        directions = get('directions', 0)
        anchor = get('anchor', (0, 0))
        angle = get('angle', 0)
        spread = get('spread', 0)
        oneByOne = get('oneByOne', False)
        anchor = tuple(get('anchor', (0, 0)))
        spawnID = get('spawnID', '')
        runner = effectsData[get('runner', None)]
        startSound = get('startSound', None)
        loopSound = get('loopSound', None)
        endSound = get('endSound', None)
        soundVolume = get('soundVolume', 0.5)
        slot = ('SLOTGUN', 'SLOTWEAPON', 'SLOTDEVICE', 'SLOTNONE').index(get('slot', 'SLOTNONE'))
        idString = data['idString']
    
    return LoadedDeviceKind

eWeapons = {}
hWeapons = {}
pGuns = [Empty]
pWeapons = [Empty]
pDevices = [Empty]

devdata = LoadCSV('data/gamedata/devices.csv')
for i in xrange(0, len(devdata)):
    cl = loadDeviceKind(devdata.getDictByIndex(i))
    name = cl.idString
    if cl.isGood:
        if cl.slot == SLOTGUN:
            pGuns.append(cl)
        elif cl.slot == SLOTWEAPON:
            pWeapons.append(cl)
        elif cl.slot == SLOTDEVICE:
            pDevices.append(cl)
        elif cl.slot == SLOTNONE:
            hWeapons[name] = cl
    else:
        eWeapons[name] = cl

global playerGuns
global playerWeapons
global playerDevices
global enemyWeapons
global helperWeapons

playerGuns = tuple(pGuns)
playerWeapons = tuple(pWeapons)
playerDevices = tuple(pDevices)
enemyWeapons = eWeapons
helperWeapons = hWeapons
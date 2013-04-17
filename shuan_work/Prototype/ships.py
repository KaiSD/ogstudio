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

def loadNPCKind(data):
    get = data.get
    
    good = get('isGood', False)
    
    imgFile = get('image', '')
    aniInfo = get('animationInfo', (1, 1, 1, True))
    img = loadAnimation(imgFile, *aniInfo)
    
    wl = []
    gl = get('weapons', [])
    widx = 1
    for i in gl:
        if good:
            wcl = helperWeapons[i]
        else:
            wcl = enemyWeapons[i]
        wx = get('weaponsX%i' % (widx), 0)
        wy = get('weaponY%i' % (widx), 0)
        wl.append(wcl(wx, wy))
        widx += 1
    
    sl = [] 
    for s in get('set', []):
        l = []
        for j in str(s):
            idx = int(j)
            if len(wl) > idx:
                if not wl[idx] in l:
                    l.append(wl[idx])
        sl.append(l)
    
    if not sl:
        sl.append(wl)
    
    class LoadedNPCKind(NPCKind):
        image = img
        brains = get('brains', [])
        life = get('life', 10)
        score = get('score', 1)
        shields = get('shield', 0)
        shieldsRegen = get('shieldsRegen', 0)
        weapons = sl[0]
        sets = sl
        idString = get('idString', '')
        isGood = good
    
    return LoadedNPCKind

devdata = LoadCSV('data/gamedata/npc.csv')
for i in xrange(0, len(devdata)):
    cl = loadNPCKind(devdata.getDictByIndex(i))
    name = cl.idString
    if cl.isGood:
        helpers[name] = cl()
    else:
        enemies[name] = cl()

playerShips += (AvatarMK1, AvatarMK2, AvatarMK3)
playerShields += (('No Shield',0,0,0), ('Shield MK1',10,1,0))
playerEngines += (('Engine MK1',5.0,12), ('Engine MK2', 10.0,50))
playerReactors += (('Reactor MK1',100), ('Reactor MK2', 150))
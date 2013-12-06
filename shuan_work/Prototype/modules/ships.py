#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype core module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from devices import *

EFFCONST = 0.25
ECOUNTCONST = 55
BASEHP = int(EFFCONST * (AGDPS+AWDPS)*60 / ECOUNTCONST)

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
        life = get('life', 1) * BASEHP
        damage = get('damage', 1) * BASEHP
        score = get('score', 1)
        shields = get('shield', 0)
        shieldsRegen = get('shieldsRegen', 0)
        weapons = sl[0]
        sets = sl
        idString = get('idString', '')
        isGood = good
    
    return LoadedNPCKind

def loadAvatarKind(data):
    get = data.get
    
    imgFile = get('image', '')
    aniInfo = get('animationInfo', (1, 1, 1, True))
    img = loadAnimation(imgFile, *aniInfo)
    
    class LoadedAvatarKind(AvatarKind):
        image = img
        life = get('life', 100)
        engine = get('engine', 1)
        name = get('name', 'Avatar')
        weaponSlots = get('weaponSlot', [])
        idString = name
    
    return LoadedAvatarKind

devdata = LoadCSV('data/gamedata/npc.csv')
for i in xrange(0, len(devdata)):
    cl = loadNPCKind(devdata.getDictByIndex(i))
    name = cl.idString
    if cl.isGood:
        helpers[name] = cl()
    else:
        enemies[name] = cl()

devdata = LoadCSV('data/gamedata/player.csv')
for i in xrange(0, len(devdata)):
    cl = loadAvatarKind(devdata.getDictByIndex(i))
    playerShips += (cl, )

devdata = LoadCSV('data/gamedata/maindevices.csv')
for i in xrange(0, len(devdata)):
    data = devdata.getDictByIndex(i)
    if data['type'] == 'Shield':
        playerShields += ((data['name'], data['param'][0], data['param'][1], data['param'][2]), )
    elif data['type'] == 'Engine':
        playerEngines += ((data['name'], data['param'][0], data['param'][1]), )
    elif data['type'] == 'Reactor':
        playerReactors += ((data['name'], data['param'][0]), )
    else:
        print 'Unknown device type:', data['type']
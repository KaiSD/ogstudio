#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype helpers module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from cocos.director import director
from cocos import collision_model, actions
from cocos.audio.pygame import mixer
from os import listdir
import pyglet
from settings import *

'''
LIBRARIES
'''
animations = {}
sounds = {}
bulletsUsed = {}
bulletsFree = {} 
shipsUsed = {}
shipsFree = {}

enemies = {}
helpers = {}
enemyWeapons = {}
helperWeapons = {}
playerShips = tuple()
playerGuns = tuple()
playerWeapons = tuple()
playerDevices = tuple()
playerShields = tuple()
playerEngines = tuple()
playerReactors = tuple()

currents = {
            'avatarObject': None,
            'layerObject': None
            }

adata = {
        None : None,
        'aMove': actions.Move(),
        'aDelay01': actions.Delay(0.1),
        'aDelay03': actions.Delay(0.3),
        'aDelay1': actions.Delay(1),
        'aDown5': actions.MoveBy((0,-900), duration=5),
        'aDown6': actions.MoveBy((0,-900), duration=6),
        'aDown9': actions.MoveBy((0,-900), duration=9),
        'aFloat60': actions.MoveBy((0,60),duration=1),
        'aFloat100': actions.MoveBy((0,100),duration=1)
        }
effectsData = {
         None: None
         }

'''
HELPERS
'''
def rel(xRel, yRel):
    return int(W*xRel), H-int(H*yRel)

def relY(yRel):
    return H-int(H*yRel)

def abs2rel(x, y):
    return x/W, 1-y/H

def loadAnimation(filename, cols, rows, period, loop=False):
    if filename == "":
        return None
    if not filename in animations.keys():
        print 'Loading', filename
        image = pyglet.image.load(filename)
        image_seq = pyglet.image.ImageGrid(image, rows, cols)
        animations[filename] = pyglet.image.Animation.from_image_sequence(image_seq, period, loop)
#    return animations[filename], filename, (cols, rows, period, loop) # TEMP
    return animations[filename]

def loadSound(filename, volume=1):
    if not Settings().sound:
#        print 'ignoring ', filename
        return
    if len(sounds) == 0:
        mixer.init()
        mixer.set_num_channels(32)
    if not filename in sounds.keys():
        sounds[filename] = mixer.Sound(filename)
    sounds[filename].set_volume(volume)
    return sounds[filename]

def playMusic(filename):
    if not Settings().music:
        return
    mixer.music.load(filename)
    mixer.music.play(-1)

def stopMusic():
    if not Settings().sound:
        return
    mixer.music.stop()

def stopAllSounds():
    if not Settings().sound:
        return
    mixer.stop()

def setCollision(spriteObject):
    size = spriteObject.get_AABB().size
    pos = spriteObject.position
    spriteObject.cshape = collision_model.AARectShape(pos, size[0]/2, size[1]/2)

def jsonLoad(filename):
    print 'Loading', filename
    try:
        f = open(filename, 'r')
        data = json.load(f)
        f.close()
        return data
    except:
        print 'BAD DATA FILE:', filename
        print exc_info()[0]
        return {}

def exportWeaponClass(cl):
    d = cl.__dict__.copy()
    filename = 'data/devices/%s.json' % (cl.__name__)
    del d['__module__']
    del d['__doc__']
    d['type'] = ('EMPTY', 'PROJECTILE', 'RAY', 'TURRET', 'SPAWN', 'AURA', 'EFFECT')[d['type'] + 1]
    if 'runner' in d:
        for k in effectsData.keys():
            if d['runner'] == effectsData[k]:
                d['runner'] = k
    import json
    f = open(filename, 'w')
    json.dump(d, f, indent = 4)
    f.close()

def exportShipClass(cl):
    def getKey(dic, val):
        for k in dic.keys():
            if dic[k] == val:
                return k
    d = cl.__dict__.copy()
    filename = 'data/ships/%s.json' % (cl.__name__)
    del d['__module__']
    del d['__doc__']
    d['image'] = d['imgFile']
    del d['imgFile']
    w = []
    for i in d.get('weapons', []):
        w.append(i.idString)
    d['weapons'] = [w]
    r = []
    for i in d.get('devices', []):
        r.append(i.idString)
    d['devices'] = r
    d['actions'] = None
    d['brains'] = [] 
            
    import json
    f = open(filename, 'w')
    json.dump(d, f, indent = 4)
    f.close()

def loadScript(filename):
    print 'Loading', filename
    try:
        f = open(filename, 'r')
        script = f.read()
        f.close()
    except:
        print 'CAN\'T READ DATA FILE:', filename
        print exc_info()[0]
        return {}
    
    stages = []
    sequences = []
    sequence = []
    key = ''
    numeric = False
    comment = False
    subLevels = []
    
    def addseq(k):
        if k == '':
            return
        if numeric:
            if '.' in k:
                k = float(k)
            else:
                k = int(k)
        if subLevels:
            subLevels[-1].append(k)
        else:
            sequence.append(k)
    
    def lst(*args):
        return args
        
    for i in script:
        if i in (',', ' ', '\r'):
            addseq(key)
            key = ''
        elif i in ('\n', ';'):
            addseq(key)
            key = ''
            if sequence:
                sequences.append(sequence[:])
                del sequence[:]
            if i == "\n":
                comment = False
        elif i == '(':
            addseq(key)
            key = ''
            subLevels.append([])
        elif i == ')':
            addseq(key)
            key = ''
            if subLevels:
                item = subLevels[-1]
                del subLevels[-1]
                if subLevels:
                    subLevels[-1].append(item)
                else:
                    sequence.append(item)
            else:
                print 'SCRIPT STRUCTURE ERROR:', filename, " - trying to close the bracket before opening it"
                return None
        elif i == '#':
            comment = True 
        elif i in ('-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'):
            if not comment:
                if key == '':
                    numeric = True
                key += i
        else:
            if not comment:
                numeric = False
                key += i
    
    if subLevels:
        print 'SCRIPT STRUCTURE ERROR:', filename, " - unclosed brackets"
        return None
    
    addseq(key)
    sequences.append(sequence)
    
    final = []
    idx = 1
    
    for s in sequences:
        if len(s) == 1:
            final.append(lst(s[0]))
        elif len(s) == 2:
            final.append(lst(s[0], *s[1]))
        else:
            print 'SCRIPT STRUCTURE ERROR:', filename, " - incorrect command length at ", idx
            return None
        idx += 1
    
    return final

def log(*args):
    if Settings().debug:
        output = u'\tDEBUG: '
        for i in args:
            output += unicode(i)
        print output
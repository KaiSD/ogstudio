#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype helpers module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from cocos.director import director
from cocos import collision_model, actions
from cocos.audio.pygame import mixer
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
followers = []

enemies = {}
helpers = {}
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

data = {
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

'''
HELPERS
'''
def rel(xRel, yRel):
    size = director.get_window_size()
    return int(size[0]*xRel), size[1]-int(size[1]*yRel)

def relY(yRel):
    size = director.get_window_size()
    return size[1]-int(size[1]*yRel)

def abs2rel(x, y):
    size = director.get_window_size()
    return x/size[0], 1-y/size[1]

def loadAnimation(filename, cols, rows, period, loop=False):
    if not filename in animations.keys():
        image = pyglet.image.load(filename)
        image_seq = pyglet.image.ImageGrid(image, rows, cols)
        animations[filename] = pyglet.image.Animation.from_image_sequence(image_seq, period, loop)
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
    try:
        f = open(filename, 'r')
        data = json.load(f)
        f.close()
        return data
    except:
        print 'BAD MISSION DATA:', filename
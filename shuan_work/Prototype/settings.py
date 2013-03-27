#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype settings module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

import json
from sys import exc_info

class Settings(object):
    obj = None
    
    width = 800
    height = 600
    
    fullscreen = False
    sound = True
    music = True
    fps = False
    
    mission = 0
    
    avatarKind = 0
    avatarEngine = 0
    avatarReactor = 0
    avatarShields = 0
    avatarGun = 0
    avatarWeapons = []
    avatarDevices = []
    
    def __new__(cls,*dt,**mp):
        '''
        Singleton checker
        '''
        if cls.obj is None:
            cls.obj = object.__new__(cls,*dt,**mp)
        return cls.obj
    
    def load(self, filename):
        try:
            f = open(filename, 'r')
            data = json.load(f)
            f.close()
            for i in data:
                if not i in ('obj', 'save', 'load') and not i[0] == '_':
                    self.__dict__[i] = data[i]
        except:
            print "Settings loading failed:", exc_info()[0]
    
    def save(self, filename):
        try:
            data = {}
            for i in self.__dict__.keys():
                if not i == 'obj':
                    data[i] = self.__dict__[i]
            f = open(filename, 'w')
            json.dump(data, f)
            f.close()
        except:
            print "Settings saving failed:", exc_info()[0]
            
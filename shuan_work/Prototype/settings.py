#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype settings module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

import json

class Settings(object):
    obj = None
    
    fullscreen = False
    sound = True
    width = 800
    height = 600
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
            pass
    
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
            pass
            
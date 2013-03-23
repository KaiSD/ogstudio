#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype core module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

import random
from mechanics import *

'''
BACKGROUNDS
'''
class Background(layer.Layer):
    def __init__(self):
        super(Background, self).__init__()
        background = sprite.Sprite('data/graphics/stars.png')
        background.position = rel(0.5, 0.5)
        self.add(background, z=0)
    def setTimeScale(self, ts, duration=0):
        pass

class AnimatedBackground(layer.Layer):
    def __init__(self):
        super(AnimatedBackground, self).__init__()
        background = sprite.Sprite('data/graphics/stars.png')
        background.position = rel(0.5, 0.5)
        self.add(background, z=0)
        img = ASprite('data/graphics/junk.png')
        img2 = ASprite('data/graphics/junk.png')
        img.position = 400, 300
        img2.position = 400, 900
        self.add(img, z=1)
        self.add(img2, z=1)
        self.scalable = [img, img2]
        act = actions.MoveBy((0, -600), duration=6)
        img.do(actions.Repeat(act + actions.Place((400, 300))))
        img2.do(actions.Repeat(act + actions.Place((400, 900))))
    def setTimeScale(self, ts, duration=0):
        if duration == 0:
            for i in self.scalable:
                i.setTimeScale(ts)
        else:
            for i in self.scalable:
                i.do(ActionFadeTimescale(ts, duration))

'''
MISSIONS
'''
class SurvivalTemplate(Mission):
    name = "Survival"
    music = 'data/music/In a Heartbeat.ogg'
    backgroundLayer = AnimatedBackground
    min = 0.05
    max = 0.5
    
    NPCKinds = (
                  enemies['Dummy'],
                  enemies['Dummy'],
                  enemies['Aimer'],
                  enemies['Aimer'],
                  enemies['Straighter'],
                  enemies['Straighter'],
                  enemies['Kami'],
                  enemies['Kami'],
                  enemies['Straighter'],
                  enemies['Straighter'],
                  enemies['Burster'],
                  enemies['Rayer'],
                  enemies['Aimer'],
                  enemies['Aimer'],
                  enemies['Straighter'],
                  enemies['Buffer'],
                  enemies['Burster'],
                  enemies['Minador'],
                  enemies['Behemoth'],
                  enemies['Summoner'],
                  )
    
    def __init__(self):
        super(SurvivalTemplate, self).__init__()
        self.ecount = len(self.NPCKinds)
    
    def logic(self, *args):
        if self.timer == 0:
            if not self.music is None:
                playMusic(self.music)
        if random.random() < min(max((self.timer + 10) / 2000.0, self.min), self.max):
            Enemy(self, self.NPCKinds[random.randint(0,int(self.timer / (10 + self.timer / self.ecount)))], random.random(), -0.1, currents['avatarObject'])
        self.timer += 1

missionsList = (SurvivalTemplate)

class SequenceTemplate(Mission):
    name = "Sequence"
    backgroundLayer = AnimatedBackground
    
    def __init__(self, sequence):
        super(SequenceTemplate, self).__init__()
        self.sequence = sequence
        
        self.nextTick = 0
        self.sequenceEntry = 0
        
        self.vars = {}
        self.labels = {}
        
        # Mission commands
        def commandComment(*args):
            pass
            
        def commandWait(*args):
            self.nextTick += int(args[0]*5)
        
        def commandSpawn(*args):
            if len(args) == 2:
                Enemy(self, enemies[args[0]], args[1], -0.1).target = currents['avatarObject']
            elif len(args) == 3:
                enemy = Enemy(self, enemies[args[0]], args[1], -0.1, currents['avatarObject'])
                meter = text.Label('',
                        font_name='Times New Roman',
                        font_size=16,
                        color = (255, 0, 0, 255),
                        anchor_x='left', anchor_y='center')
                meter.position = rel(0.8,0.05*(len(self.meters)+1)+0.05)
                self.add(meter, z=10)
                self.namedEnemies[args[2]] = enemy
                self.meters[args[2]] = meter
            else:
                Enemy(self, enemies[args[0]], random.random(), -0.1).target = currents['avatarObject']
        
        def commandWaitHealth(*args):
            if len(args) == 1:
                if args[0] in self.namedEnemies:
                    if self.namedEnemies[args[0]].life > 0:
                        self.sequenceEntry -= 1
                    else:
                        self.meters[args[0]].kill()
                        del self.meters[args[0]]
                        del self.namedEnemies[args[0]]
            if len(args) == 2:
                if args[0] in self.namedEnemies:
                    if self.namedEnemies[args[0]].life > args[1]:
                        self.sequenceEntry -= 1
                    elif self.namedEnemies[args[0]].life <= 0:
                        self.meters[args[0]].kill()
                        del self.meters[args[0]]
                        del self.namedEnemies[args[0]]
        
        def commandSwitchBrains(*args):
            if len(args) == 2:
                if args[0] in self.namedEnemies:
                    self.namedEnemies[args[0]].switchBrains(self.namedEnemies[args[0]], args[1])
        
        def commandMusic(*args):
            if len(args) == 1:
                stopMusic()
                playMusic(args[0])
        
        def commandBackgroundSpeed(*args):
            if len(args) == 1:
                self.backgroundLayer.setTimeScale(args[0])
            elif len(args) == 2:
                self.backgroundLayer.setTimeScale(args[0], args[1])
        
        def commandSetVar(*args):
            if len(args) == 2:
                if type(args[1]) == str and args[1] in self.vars:
                    self.vars[args[0]] = self.vars[args[1]]
                else:
                    self.vars[args[0]] = args[1]
        
        def commandIncVar(*args):
            if len(args) == 2:
                if args[0] in self.vars:
                    if type(args[1]) == str and args[1] in self.vars:
                        self.vars[args[0]] += self.vars[args[1]]
                    else:
                        self.vars[args[0]] += args[1]
        
        def commandCheckVar(*args):
            if len(args) >= 2:
                if args[0] in self.vars:
                    src = self.vars[args[0]]
                    target = None
                    if args[0] in self.vars:
                        if type(args[1]) == str and args[1] in self.vars:
                            target = self.vars[args[1]]
                        else:
                            target = args[1]
                    if not src == target:
                        if len(args) == 3:
                            self.sequenceEntry += args[2]
                        else:
                            self.sequenceEntry += 1
        
        def commandCheckHealth(*args):
            if len(args) == 1:
                if args[0] in self.namedEnemies:
                    if self.namedEnemies[args[0]].life > 0:
                        self.sequenceEntry -= 1
                    else:
                        self.meters[args[0]].kill()
                        del self.meters[args[0]]
                        del self.namedEnemies[args[0]]
            if len(args) == 2:
                if args[0] in self.namedEnemies:
                    if self.namedEnemies[args[0]].life > args[1]:
                        self.sequenceEntry -= 1
                    elif self.namedEnemies[args[0]].life <= 0:
                        self.meters[args[0]].kill()
                        del self.meters[args[0]]
                        del self.namedEnemies[args[0]]

        def commandShift(*args):
            if len(args) == 1:
                self.sequenceEntry += args[0]
        
        def commandSetLable(*args):
            if len(args) == 1:
                self.labels[args[0]] = self.sequenceEntry
        
        def commandToLable(*args):
            if len(args) == 1:
                if args[0] in self.labels:
                    self.sequenceEntry = self.labels[args[0]]
        
        self.MissionCommands = {
                           'Comment':commandComment,
                           'Wait':commandWait,
                           'Spawn':commandSpawn,
                           'WaitEnemyHealth':commandWaitHealth,
                           'SwitchBrains':commandSwitchBrains,
                           'Music':commandMusic,
                           'BackgroundSpeed':commandBackgroundSpeed,
                           'Var':commandSetVar,
                           'IncVar':commandIncVar,
                           'CheckVar':commandCheckVar,
                           'WaitEnemyHealth':commandCheckHealth,
                           'Shift':commandShift,
                           'Mark':commandSetLable,
                           'ToMark':commandToLable,
                           }
    
    def reset(self):
        self.__init__(self.sequence)
    
    def logic(self, *args):
        # Keep going
        if self.timer == self.nextTick:
            if self.sequenceEntry < len(self.sequence):
                command = self.sequence[self.sequenceEntry]
                self.MissionCommands[command[0]](*command[1:])
                self.nextTick += 1
                self.sequenceEntry += 1
            else:
                self.missionCompleted()
        self.timer += 1
        # Update vars
        self.vars['_AvatarHealth_'] = currents['avatarObject'].life
        self.vars['_AvatarHPosition_'], self.vars['_AvatarVPosition_'] = abs2rel(*currents['avatarObject'].position)
        self.vars['_Score_'] = self.score
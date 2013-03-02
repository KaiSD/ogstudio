#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

import os
import coui
from sys import exit
from missions import *

VERSION = '0.4'
missionsList = []
pyglet.options['debug_gl'] = False

'''
MAIN MENU TREE
'''
class Start(layer.Layer):
    is_event_handler = True
    
    def __init__(self):
        super(Start, self).__init__()
        label = text.Label('Press any key.',
                     font_name='Times New Roman',
                     font_size=32,
                     anchor_x='center', anchor_y='center')
        label.position = rel(0.5, 0.8)
        self.add(label, z=1)
        scale = actions.ScaleBy(1.1, duration=1)
        label.do(actions.Repeat(scale + actions.Reverse(scale)))
        logo = sprite.Sprite('data/graphics/Shuan2D.png')
        logo.position = rel(0.5,0.2)
        self.add(logo, z=1)
    
    def on_key_release (self, key, modifiers):
        self.start()
    
    def on_mouse_release (self, x, y, buttons, modifiers):
        self.start()
    
    def start(self):
        director.replace(scene.Scene(Background(), MainMenu()))

class MainMenu(layer.Layer):
    def __init__(self):
        super(MainMenu, self).__init__()
        logo = sprite.Sprite('data/graphics/Shuan2D.png')
        logo.position = rel(0.65,0.3)
        self.add(logo, z=1)
        # Menu UI
        gui = coui.CocosUIFrame()
        pos = rel(0.1, 0.25)
        dia = coui.Dialogue('Menu', name='Menu', moveable=False, x=pos[0], y=pos[1], content=
        coui.VLayout(children=[
            coui.Button('Start', action = self.startGame),
            coui.Button('Mission', action = self.missions),
            coui.Button('Ship', action = self.ships),
            coui.Button('Options', action = self.options),
            coui.Button('Quit', action = self.quit),
            ])
        )
        gui.add(dia)
        self.add(gui, z=99)
    
    def quit(self, *args):
        director.terminate_app = True
    
    def startGame(self, *args):
        mission = missionsList[Settings().mission]
        mission.setup()
        background = mission.backgroundLayer()
        game = Game(background, mission)
        director.replace(scenes.FadeDownTransition(game, duration=2))
    
    def options(self, *args):
        director.push(scene.Scene(Background(), Options()))
    
    def missions(self, *args):
        director.push(scene.Scene(Background(), Missions()))
    
    def ships(self, *args):
        director.push(scene.Scene(Background(), Ships()))

class Options(layer.Layer):
    def __init__(self):
        super(Options, self).__init__()
        logo = sprite.Sprite('data/graphics/Shuan2D.png')
        logo.position = rel(0.65,0.3)
        self.add(logo, z=1)
        # Options UI
        gui = coui.CocosUIFrame()
        pos = rel(0.1, 0.25)
        dia = coui.Dialogue('Options', name='Options', moveable=False, x=pos[0], y=pos[1], content=
        coui.VLayout(children=[
            coui.Checkbox('Fullscreen', h=100, value=settings.fullscreen, action=self.changeFullScreen),
            coui.Checkbox('Sounds', h=100, value=settings.sound, action=self.changeSound),
            coui.Checkbox('FPS', h=100, value=settings.fps, action=self.changeFPS),
            coui.Button('Back', action = self.back),
            ])
        )
        gui.add(dia)
        self.add(gui, z=99)
        
    
    def back(self, *args):
        director.pop()
    
    def changeFullScreen(self, *args):
        if settings.fullscreen == True:
            settings.fullscreen = False
            director.window.set_fullscreen(False)
        else:
            settings.fullscreen = True
            director.window.set_fullscreen(True)
    
    def changeSound(self, *args):
        if settings.sound == True:
            settings.sound = False
        else:
            settings.sound = True
    
    def changeFPS(self, *args):
        if settings.fps == True:
            director.show_FPS = False
            settings.fps = False
        else:
            director.show_FPS = True
            settings.fps = True

class Missions(layer.Layer):
    def __init__(self):
        super(Missions, self).__init__()
        logo = sprite.Sprite('data/graphics/Shuan2D.png')
        logo.position = rel(0.65,0.3)
        self.add(logo, z=1)
        #Missions list
        l = [coui.Label('Current mission:'),
             coui.Label(missionsList[settings.mission].name, name='Current')
             ]
        for i in xrange(0, len(missionsList)):
            m = missionsList[i]
            l.append( coui.Button(m.name, action=self.SetMissionConstructor(i)))
        l.append( coui.Button('Back', action = self.back))
        # Missions UI
        self.gui = coui.CocosUIFrame()
        pos = rel(0.1, 0.25)
        dia = coui.Dialogue('Missions', name='Missions', moveable=False, x=pos[0], y=pos[1], content=
        coui.VLayout(children=l)
        )
        self.gui.add(dia)
        self.add(self.gui, z=99)
    
    def SetMissionConstructor(self, idx):
        def setMission(*args):
            settings.mission = idx
            self.gui.get_element_by_name('Current').text = missionsList[idx].name
        return setMission
    
    def back(self, button):
        director.pop()

class Ships(layer.Layer):
    def __init__(self):
        super(Ships, self).__init__()
        logo = sprite.Sprite('data/graphics/Shuan2D.png')
        logo.position = rel(0.65,0.3)
        self.add(logo, z=1)
        # Ships, weapons and devices list
        # Ships UI
        self.gui = coui.CocosUIFrame()
        pos = rel(0.1, 0.1)
        dia = coui.Dialogue('Ship settings', name='Ship', moveable=False, x=pos[0], y=pos[1], content=
        coui.VLayout(children=[
            coui.HLayout(children=[
                   coui.VLayout(children=[
                        coui.Label('Current ship'),
                        coui.Button(playerShips[settings.avatarKind].name, action=self.cycleShips, name="ShipSelector"),
                        coui.HLayout(children=[coui.Button(playerShields[settings.avatarShields][0], name="ShieldSelector", action=self.cycleShields),
                        coui.Button(playerReactors[settings.avatarReactor][0], name="ReactorSelector", action=self.cycleReactors)]),
                        coui.Button(playerEngines[settings.avatarEngine][0], name="EngineSelector", action=self.cycleEngines),
                        coui.Label('Main gun'),
                        coui.Button(playerGuns[settings.avatarGun].name, action=self.cycleGuns, name="GunSelector"),
                        coui.Label('Additional weapons'),
                        coui.Button('Weapon', name="Weapon1Selector", action=self.cycleWeaponConstructor(1)),
                        coui.Button('Weapon', name="Weapon2Selector", action=self.cycleWeaponConstructor(2)),
                        coui.Button('Weapon', name="Weapon3Selector", action=self.cycleWeaponConstructor(3)),
                        coui.Button('Weapon', name="Weapon4Selector", action=self.cycleWeaponConstructor(4)),
                        coui.Button('Weapon', name="Weapon5Selector", action=self.cycleWeaponConstructor(5)),
                        coui.Label('Devices'),
                        coui.Label('Can\'t change devices'),
                        ]),
                   coui.FlowLayout(w=300, children=[
                        coui.Label('Credits ($):'),
                        coui.Label('0', name='Money'),
                        coui.Label('Maneuverability Class:'),
                        coui.Label('1', name='Speed'),
                        coui.Label('Armor durability (du):'),
                        coui.Label('100', name='Armor'),
                        coui.Label('Shields power (du):'),
                        coui.Label('0', name='Shield'),
                        coui.Label('Shields regen (du/s):'),
                        coui.Label('0', name='Regen'),
                        coui.Label('Energy production:'),
                        coui.Label('150', name='PowerIn'),
                        coui.Label('Energy consumption:'),
                        coui.Label('130', name='PowerOut')
                        ])
                   ]),
            coui.Button('Back', action = self.back),
            ])
        )
        self.gui.add(dia)
        
        element = self.gui.get_element_by_name('Weapon5Selector')
        if len(playerShips[settings.avatarKind].weaponSlots) >= 7:
            while len(settings.avatarWeapons) < 5:
                settings.avatarWeapons.append(0)
            element.text = playerWeapons[settings.avatarWeapons[4]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon4Selector')
        if len(playerShips[settings.avatarKind].weaponSlots) >= 6:
            while len(settings.avatarWeapons) < 4:
                settings.avatarWeapons.append(0)
            element.text = playerWeapons[settings.avatarWeapons[3]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon3Selector')
        if len(playerShips[settings.avatarKind].weaponSlots) >= 5:
            while len(settings.avatarWeapons) < 3:
                settings.avatarWeapons.append(0)
            element.text = playerWeapons[settings.avatarWeapons[2]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon2Selector')
        if len(playerShips[settings.avatarKind].weaponSlots) >= 4:
            while len(settings.avatarWeapons) < 2:
                settings.avatarWeapons.append(0)
            element.text = playerWeapons[settings.avatarWeapons[1]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon1Selector')
        if len(settings.avatarWeapons) < 1:
                settings.avatarWeapons.append(0)
        element.text = playerWeapons[settings.avatarWeapons[0]].name
        
        self.add(self.gui, z=99)
    
    def cycleShips(self, *args):
        if settings.avatarKind < len(playerShips) - 1:
            settings.avatarKind += 1
        else:
            settings.avatarKind = 0
        
        element = self.gui.get_element_by_name('ShipSelector')
        element.text = playerShips[settings.avatarKind].name
        element = self.gui.get_element_by_name('Weapon5Selector')
        if len(playerShips[settings.avatarKind].weaponSlots) >= 7:
            if len(settings.avatarWeapons) < 5:
                settings.avatarWeapons.append(0)
            element.text = playerWeapons[settings.avatarWeapons[4]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon4Selector')
        if len(playerShips[settings.avatarKind].weaponSlots) >= 6:
            if len(settings.avatarWeapons) < 4:
                settings.avatarWeapons.append(0)
            element.text = playerWeapons[settings.avatarWeapons[3]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon3Selector')
        if len(playerShips[settings.avatarKind].weaponSlots) >= 5:
            if len(settings.avatarWeapons) < 3:
                settings.avatarWeapons.append(0)
            element.text = playerWeapons[settings.avatarWeapons[2]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon2Selector')
        if len(playerShips[settings.avatarKind].weaponSlots) >= 4:
            if len(settings.avatarWeapons) < 2:
                settings.avatarWeapons.append(0)
            element.text = playerWeapons[settings.avatarWeapons[1]].name
            element.visible = True
        else:
            element.visible = False
    
    def cycleShields(self, *args):
        if settings.avatarShields < len(playerShields) - 1:
            settings.avatarShields += 1
        else:
            settings.avatarShields = 0
        element = self.gui.get_element_by_name('ShieldSelector')
        element.text = playerShields[settings.avatarShields][0]
        self.gui.ui.update_layout()
    
    def cycleReactors(self, *args):
        if settings.avatarReactor < len(playerReactors) - 1:
            settings.avatarReactor += 1
        else:
            settings.avatarReactor = 0
        element = self.gui.get_element_by_name('ReactorSelector')
        element.text = playerReactors[settings.avatarReactor][0]
        self.gui.ui.update_layout()
    
    def cycleEngines(self, *args):
        if settings.avatarEngine < len(playerEngines) - 1:
            settings.avatarEngine += 1
        else:
            settings.avatarEngine = 0
        element = self.gui.get_element_by_name('EngineSelector')
        element.text = playerEngines[settings.avatarEngine][0]
        self.gui.ui.update_layout()
    
    def cycleGuns(self, *args):
        if settings.avatarGun < len(playerGuns) - 1:
            settings.avatarGun += 1
        else:
            settings.avatarGun = 0
        element = self.gui.get_element_by_name('GunSelector')
        element.text = playerGuns[settings.avatarGun].name
        self.gui.ui.update_layout()
    
    def cycleWeaponConstructor(self, idx):
        def cycleWeapon(*args):
            while len(settings.avatarWeapons) < idx:
                settings.avatarWeapons.append(0)
            if settings.avatarWeapons[idx - 1] < len(playerWeapons) - 1:
                settings.avatarWeapons[idx - 1] += 1
            else:
                settings.avatarWeapons[idx - 1] = 0
            element = self.gui.get_element_by_name('Weapon' + str(idx) + 'Selector')
            element.text = playerWeapons[settings.avatarWeapons[idx - 1]].name
            self.gui.ui.update_layout()
        
        return cycleWeapon

    
    def back(self, *args):
        director.pop()

if __name__ == "__main__":
    settings = Settings()
    settings.load('.settings')
    director.init(width=settings.width, height=settings.height, caption="Shuan 2D " + VERSION, fullscreen=settings.fullscreen, vsync=False)
    
    missionsList.append(SurvivalTemplate())
    for i in os.listdir('data/missions'):
        if i.endswith('.seq'):
            m = SequenceTemplate(jsonLoad('data/missions/'+i))
            if m.sequence is None:
                exit(1)
            m.name = i[:-4]
            missionsList.append(m)
    
    startMenu = scene.Scene(Background(), Start())
    director.show_FPS = settings.fps
    director.run(startMenu)
    settings.save('.settings')
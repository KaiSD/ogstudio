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
CPROFILE = True
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
            coui.Button('About', action = self.about),
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
    
    def about(self, *args):
        director.push(scene.Scene(Background(), About()))
    
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
            coui.Checkbox('Fullscreen', h=100, value=Settings().fullscreen, action=self.changeFullScreen),
            coui.Checkbox('Sounds', h=100, value=Settings().sound, action=self.changeSound),
            coui.Checkbox('Music', h=100, value=Settings().music, action=self.changeMusic),
            coui.Checkbox('FPS', h=100, value=Settings().fps, action=self.changeFPS),
            coui.Button('Back', action = self.back),
            ])
        )
        gui.add(dia)
        self.add(gui, z=99)
        
    
    def back(self, *args):
        director.pop()
        Settings().save('.settings')
    
    def changeFullScreen(self, *args):
        if Settings().fullscreen == True:
            Settings().fullscreen = False
            director.window.set_fullscreen(False)
        else:
            Settings().fullscreen = True
            director.window.set_fullscreen(True)
    
    def changeSound(self, *args):
        if Settings().sound == True:
            Settings().sound = False
        else:
            Settings().sound = True
    
    def changeMusic(self, *args):
        if Settings().music == True:
            Settings().music = False
        else:
            Settings().music = True

    def changeFPS(self, *args):
        if Settings().fps == True:
            director.show_FPS = False
            Settings().fps = False
        else:
            director.show_FPS = True
            Settings().fps = True

class Missions(layer.Layer):
    def __init__(self):
        super(Missions, self).__init__()
        logo = sprite.Sprite('data/graphics/Shuan2D.png')
        logo.position = rel(0.65,0.3)
        self.add(logo, z=1)
        #Missions list
        l = [coui.Label('Current mission:'),
             coui.Label(missionsList[Settings().mission].name, name='Current')
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
            Settings().mission = idx
            self.gui.get_element_by_name('Current').text = missionsList[idx].name
        return setMission
    
    def back(self, button):
        director.pop()
        Settings().save('.settings')

class About(layer.Layer):
    def __init__(self):
        super(About, self).__init__()
        logo = sprite.Sprite('data/graphics/Shuan2D.png')
        logo.position = rel(0.65,0.3)
        self.add(logo, z=1)
        # Ships, weapons and devices list
        # Ships UI
        self.gui = coui.CocosUIFrame()
        pos = rel(0.1, 0.1)
        dia = coui.Dialogue('Shuan 2D gameplay prototype', moveable=False, x=pos[0], y=pos[1], content=
        coui.VLayout(children=[
            coui.Label('This is not a game, it\'s a playable prototype,'),
            coui.Label('To find a latest news about the game, visit the Opensource Game Studio Website.'),
            coui.Label(''),
            coui.Label('(с) 2012-2013 Opensource Game Studio'),
            coui.Label('License: GPL v3'),
            coui.Label('Third party graphics used:'),
            coui.Label('"SpriteLib" by Ari Feldman (http://www.widgetworx.com)'),
            coui.Label('"Spaceships" and "Fighters" by Skorpio (http://opengameart.org/users/skorpio)'),
            coui.Label('"Free Airplane Sprite" by Mark Simpson (http://prinzeugn.deviantart.com/)'),
            coui.Label('Music:'),
            coui.Label('"In a Heartbeat" by Kevin MacLeod is licensed under a CC Attribution 3.0.'),
            coui.Button('Back', action = self.back),
            ])
        )
        self.gui.add(dia)
        self.add(self.gui, z=99)
    
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
                        coui.Button(playerShips[Settings().avatarKind].name, action=self.cycleShips, name="ShipSelector"),
                        coui.HLayout(children=[coui.Button(playerShields[Settings().avatarShields][0], name="ShieldSelector", action=self.cycleShields),
                        coui.Button(playerReactors[Settings().avatarReactor][0], name="ReactorSelector", action=self.cycleReactors)]),
                        coui.Button(playerEngines[Settings().avatarEngine][0], name="EngineSelector", action=self.cycleEngines),
                        coui.Label('Main gun'),
                        coui.Button(playerGuns[Settings().avatarGun].name, action=self.cycleGuns, name="GunSelector"),
                        coui.Label('Additional weapons'),
                        coui.Button('Weapon', name="Weapon1Selector", action=self.cycleWeaponConstructor(1)),
                        coui.HLayout(children=[
                        coui.Button('Weapon', name="Weapon2Selector", action=self.cycleWeaponConstructor(2)),
                        coui.Button('Weapon', name="Weapon3Selector", action=self.cycleWeaponConstructor(3))
                        ]),
                        coui.HLayout(children=[
                        coui.Button('Weapon', name="Weapon4Selector", action=self.cycleWeaponConstructor(4)),
                        coui.Button('Weapon', name="Weapon5Selector", action=self.cycleWeaponConstructor(5))
                        ]),
                        coui.Label('Devices'),
                        coui.Button('Device', name="Device1Selector", action=self.cycleDeviceConstructor(1)),
                        coui.Button('Device', name="Device2Selector", action=self.cycleDeviceConstructor(2)),
                        coui.Button('Device', name="Device3Selector", action=self.cycleDeviceConstructor(3))
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
                        coui.Label('130', name='PowerOut'),
                        coui.Label('Peak energy consumption:'),
                        coui.Label('130', name='PeakPowerOut')
                        ])
                   ]),
            coui.Button('Back', action = self.back),
            ])
        )
        self.gui.add(dia)
        
        element = self.gui.get_element_by_name('Weapon5Selector')
        if len(playerShips[Settings().avatarKind].weaponSlots) >= 7:
            while len(Settings().avatarWeapons) < 5:
                Settings().avatarWeapons.append(0)
            element.text = playerWeapons[Settings().avatarWeapons[4]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon4Selector')
        if len(playerShips[Settings().avatarKind].weaponSlots) >= 6:
            while len(Settings().avatarWeapons) < 4:
                Settings().avatarWeapons.append(0)
            element.text = playerWeapons[Settings().avatarWeapons[3]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon3Selector')
        if len(playerShips[Settings().avatarKind].weaponSlots) >= 5:
            while len(Settings().avatarWeapons) < 3:
                Settings().avatarWeapons.append(0)
            element.text = playerWeapons[Settings().avatarWeapons[2]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon2Selector')
        if len(playerShips[Settings().avatarKind].weaponSlots) >= 4:
            while len(Settings().avatarWeapons) < 2:
                Settings().avatarWeapons.append(0)
            element.text = playerWeapons[Settings().avatarWeapons[1]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon1Selector')
        if len(Settings().avatarWeapons) < 1:
                Settings().avatarWeapons.append(0)
        element.text = playerWeapons[Settings().avatarWeapons[0]].name
        
        element = self.gui.get_element_by_name('Device3Selector')
        if len(playerShips[Settings().avatarKind].deviceSlots) >= 3:
            while len(Settings().avatarDevices) < 3:
                Settings().avatarDevices.append(0)
            element.text = playerDevices[Settings().avatarDevices[2]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Device2Selector')
        if len(playerShips[Settings().avatarKind].deviceSlots) >= 2:
            while len(Settings().avatarDevices) < 2:
                Settings().avatarDevices.append(0)
            element.text = playerDevices[Settings().avatarDevices[1]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Device1Selector')
        if len(Settings().avatarDevices) < 1:
                Settings().avatarDevices.append(0)
        element.text = playerDevices[Settings().avatarDevices[0]].name
        
        self.add(self.gui, z=99)
    
    def cycleShips(self, *args):
        if Settings().avatarKind < len(playerShips) - 1:
            Settings().avatarKind += 1
        else:
            Settings().avatarKind = 0
        
        element = self.gui.get_element_by_name('ShipSelector')
        element.text = playerShips[Settings().avatarKind].name
        element = self.gui.get_element_by_name('Weapon5Selector')
        if len(playerShips[Settings().avatarKind].weaponSlots) >= 7:
            if len(Settings().avatarWeapons) < 5:
                Settings().avatarWeapons.append(0)
            element.text = playerWeapons[Settings().avatarWeapons[4]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon4Selector')
        if len(playerShips[Settings().avatarKind].weaponSlots) >= 6:
            if len(Settings().avatarWeapons) < 4:
                Settings().avatarWeapons.append(0)
            element.text = playerWeapons[Settings().avatarWeapons[3]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon3Selector')
        if len(playerShips[Settings().avatarKind].weaponSlots) >= 5:
            if len(Settings().avatarWeapons) < 3:
                Settings().avatarWeapons.append(0)
            element.text = playerWeapons[Settings().avatarWeapons[2]].name
            element.visible = True
        else:
            element.visible = False
        element = self.gui.get_element_by_name('Weapon2Selector')
        if len(playerShips[Settings().avatarKind].weaponSlots) >= 4:
            if len(Settings().avatarWeapons) < 2:
                Settings().avatarWeapons.append(0)
            element.text = playerWeapons[Settings().avatarWeapons[1]].name
            element.visible = True
        else:
            element.visible = False
    
    def cycleShields(self, *args):
        if Settings().avatarShields < len(playerShields) - 1:
            Settings().avatarShields += 1
        else:
            Settings().avatarShields = 0
        element = self.gui.get_element_by_name('ShieldSelector')
        element.text = playerShields[Settings().avatarShields][0]
        self.gui.ui.update_layout()
    
    def cycleReactors(self, *args):
        if Settings().avatarReactor < len(playerReactors) - 1:
            Settings().avatarReactor += 1
        else:
            Settings().avatarReactor = 0
        element = self.gui.get_element_by_name('ReactorSelector')
        element.text = playerReactors[Settings().avatarReactor][0]
        self.gui.ui.update_layout()
    
    def cycleEngines(self, *args):
        if Settings().avatarEngine < len(playerEngines) - 1:
            Settings().avatarEngine += 1
        else:
            Settings().avatarEngine = 0
        element = self.gui.get_element_by_name('EngineSelector')
        element.text = playerEngines[Settings().avatarEngine][0]
        self.gui.ui.update_layout()
    
    def cycleGuns(self, *args):
        if Settings().avatarGun < len(playerGuns) - 1:
            Settings().avatarGun += 1
        else:
            Settings().avatarGun = 0
        element = self.gui.get_element_by_name('GunSelector')
        element.text = playerGuns[Settings().avatarGun].name
        self.gui.ui.update_layout()
    
    def cycleWeaponConstructor(self, idx):
        def cycleWeapon(*args):
            while len(Settings().avatarWeapons) < idx:
                Settings().avatarWeapons.append(0)
            if Settings().avatarWeapons[idx - 1] < len(playerWeapons) - 1:
                Settings().avatarWeapons[idx - 1] += 1
            else:
                Settings().avatarWeapons[idx - 1] = 0
            element = self.gui.get_element_by_name('Weapon' + str(idx) + 'Selector')
            element.text = playerWeapons[Settings().avatarWeapons[idx - 1]].name
            self.gui.ui.update_layout()
        
        return cycleWeapon
    
    def cycleDeviceConstructor(self, idx):
        def cycleDevice(*args):
            while len(Settings().avatarDevices) < idx:
                Settings().avatarDevices.append(0)
            if Settings().avatarDevices[idx - 1] < len(playerDevices) - 1:
                Settings().avatarDevices[idx - 1] += 1
            else:
                Settings().avatarDevices[idx - 1] = 0
            element = self.gui.get_element_by_name('Device' + str(idx) + 'Selector')
            element.text = playerDevices[Settings().avatarDevices[idx - 1]].name
            self.gui.ui.update_layout()
        
        return cycleDevice

    def back(self, *args):
        director.pop()
        Settings().save('.settings')

if __name__ == "__main__":
    settings = Settings()
    Settings().load('.settings')
    director.init(width=Settings().width, height=Settings().height, caption="Shuan 2D " + VERSION, fullscreen=Settings().fullscreen, vsync=False)
    
    missionsList.append(SurvivalTemplate())
    for i in os.listdir('data/missions'):
        if i.endswith('.seq'):
            m = SequenceTemplate(jsonLoad('data/missions/'+i))
            if m.sequence is None:
                exit(1)
            m.name = i[:-4]
            missionsList.append(m)
    
    startMenu = scene.Scene(Background(), Start())
    director.show_FPS = Settings().fps
    if CPROFILE:
        import cProfile
        cProfile.run('director.run(startMenu)', 'gameinfo.profile')
    else:
        director.run(startMenu)
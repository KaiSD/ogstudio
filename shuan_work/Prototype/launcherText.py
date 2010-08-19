# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launcher.ui'
#
# Created: Sat Aug 14 23:31:38 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

import sys, os, os.path
import game

class Main(object):
    def __init__(self):
        self.missions = []
        self.ships = []
        self.guns = []
        self.weapons = []
        self.heavy = []
        
        for i in os.listdir('Modules'):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.missions.append(i[:-3])
        print 'Missions:'
        c = 0
        for i in self.missions:
            print c, i
            c += 1
        self.selectedMission = self.missions[int(raw_input('Mission number: '))] 
    
        for i in os.listdir(os.path.join('Modules', 'Avatars')):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.ships.append(i[:-3])
        print 'Ships:'
        c = 0
        for i in self.ships:
            print c, i
            c += 1
        self.selectedShip = self.ships[int(raw_input('Ship number: '))] 
        
        print 'Upgrades:'
        self.shield = int(raw_input('Shields (0-6): '))
        self.ammo = int(raw_input('Heavy ammo (0-6): '))
        self.reactor = int(raw_input('Reactor (0-6): '))
        
        for i in os.listdir(os.path.join('Modules', 'Guns')):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.guns.append(i[:-3])
        print 'Guns:'
        c = 0
        for i in self.guns:
            print c, i
            c += 1
        self.selectedGun = self.guns[int(raw_input('Gun number: '))]
        
        for i in os.listdir(os.path.join('Modules', 'Weapons')):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.weapons.append(i[:-3])
        self.selectedWeapons = []
        while True:
            print 'Light weapons:'
            c = 0
            for i in self.weapons:
                print c, i
                c += 1
            sel = int(raw_input('Weapon number (-1 to finish): '))
            if sel < 0:
                break
            else:
                self.selectedWeapons.append(self.weapons[sel])
                print self.weapons[sel], 'added'
    
        for i in os.listdir(os.path.join('Modules', 'HeavyWeapons')):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.heavy.append(i[:-3])
        print 'Heavy weapons:'
        c = 0
        for i in self.heavy:
            print c, i
            c += 1
        self.selectedHeavy = self.heavy[int(raw_input('Weapon number: '))] 
    
    def launch(self):
        mission = str(self.selectedMission)
        ship = str(self.selectedShip)
        heavy = str(self.selectedHeavy)
        weapons = self.selectedWeapons
        gun = str(self.selectedGun)
        shield = int(self.shield)
        ammo = int(self.ammo)
        reactor = int(self.reactor)
        
        game.main(mission=mission, playerShip=ship, playerWeapons=weapons, playerGun=gun, playerHeavyWeapon=heavy,
                  playerShield=shield, playerAmmo=ammo, playerReactor=reactor)

if __name__ == "__main__":
    launcher = Main()
    launcher.launch()


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launcher.ui'
#
# Created: Sat Aug 14 23:31:38 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, uic
import sys, os.path
import pygame
import game
import config

# Select to search for py or pyc files for weapons and missions lists 
packed = True

class Main(QtCore.QObject):
    def __init__(self, packed=False):
        QtCore.QObject.__init__(self)
        self.ui = uic.loadUi('launcher.ui', baseinstance=None)
        
        # Flags
        self.packed = packed
        
        # Initializing
        pygame.init()
        bestdepth = pygame.display.mode_ok((config.screenWidth, config.screenHeight), 0, 32)
        self.screen = pygame.display.set_mode((config.screenWidth, config.screenHeight), 0, bestdepth)
        self.loader()
        
        # Connectors
        self.ui.pushButtonLaunch.clicked.connect(self.launch)
        self.ui.pushButtonAddWeapon.clicked.connect(self.addWeapon)
        self.ui.pushButtonRemoveWeapon.clicked.connect(self.removeWeapon)
        self.ui.comboBoxReactor.currentIndexChanged.connect(self.refreshEnergy)
        self.ui.comboBoxShields.currentIndexChanged.connect(self.refreshEnergy)
        self.ui.comboBoxGun.currentIndexChanged.connect(self.refreshEnergy)
        self.ui.comboBoxAmmo.currentIndexChanged.connect(self.refreshEnergy)
        
        self.refreshEnergy()
    
    def loader(self):
        if self.packed:
            ext = '.pyc'
            d = -4
        else:
            ext = '.py'
            d = -3
        for i in os.listdir('Modules'):
            if i.endswith(ext) and not i.startswith('__init__'):
                __import__('Modules.'+i[:d])
                self.ui.comboBoxMission.addItem(QtCore.QString(i[:d]))
        
        for i in os.listdir(os.path.join('Modules', 'Avatars')):
            if i.endswith(ext) and not i.startswith('__init__'):
                __import__('Modules.Avatars.'+i[:d])
                self.ui.comboBoxShip.addItem(QtCore.QString(i[:d]))
        
        for i in os.listdir(os.path.join('Modules', 'Guns')):
            if i.endswith(ext) and not i.startswith('__init__'):
                __import__('Modules.Guns.'+i[:d])
                self.ui.comboBoxGun.addItem(QtCore.QString(i[:d]))
        
        for i in os.listdir(os.path.join('Modules', 'Weapons')):
            if i.endswith(ext) and not i.startswith('__init__'):
                __import__('Modules.Weapons.'+i[:d])
                self.ui.comboBoxWeapons.addItem(QtCore.QString(i[:d]))
    
        for i in os.listdir(os.path.join('Modules', 'HeavyWeapons')):
            if i.endswith(ext) and not i.startswith('__init__'):
                __import__('Modules.HeavyWeapons.'+i[:d])
                self.ui.comboBoxHeavy.addItem(QtCore.QString(i[:d]))                
    
    def launch(self):
        mission = str(self.ui.comboBoxMission.currentText())
        ship = str(self.ui.comboBoxShip.currentText())
        heavy = str(self.ui.comboBoxHeavy.currentText())
        gun = str(self.ui.comboBoxGun.currentText())
        shield = int(self.ui.comboBoxShields.currentText())
        ammo = int(self.ui.comboBoxAmmo.currentText())
        reactor = int(self.ui.comboBoxReactor.currentText())
        weapons = []
        for i in xrange(0, self.ui.listWidget.count()):
            weapons.append(str(self.ui.listWidget.takeItem(0).text()))
        self.ui.close()
        pygame.mixer.init(44100, -16, 2, 512)
        game.main(self.screen, mission=mission, playerShip=ship, playerWeapons=weapons, playerGun=gun, playerHeavyWeapon=heavy,
                  playerShield=shield, playerAmmo=ammo, playerReactor=reactor)
        self.ui.show()
    
    def addWeapon(self):
        weapon = self.ui.comboBoxWeapons.currentText()
        self.ui.listWidget.addItem(weapon)
        self.refreshEnergy()
    
    def removeWeapon(self):
        index = self.ui.listWidget.currentRow()
        self.ui.listWidget.takeItem(index)
        self.refreshEnergy()
    
    def refreshEnergy(self):
        energy = 100+50*int(self.ui.comboBoxReactor.currentText())
        costs = 20 * int(self.ui.comboBoxShields.currentText()) + 10* int(self.ui.comboBoxAmmo.currentText())
        gun = str(self.ui.comboBoxGun.currentText())
        if len(gun) == 0:
            self.ui.lineEditReactor.setText(QtCore.QString(str(costs)+'/'+str(energy)))
            return
        gunClass = __import__('Modules.Guns.'+gun, globals(), locals(), ['Weapon'], -1).Weapon
        costs += gunClass.energyCost*2
        for i in xrange(0, self.ui.listWidget.count()):
            weapon = str(self.ui.listWidget.item(i).text())
            weaponClass = __import__('Modules.Weapons.'+weapon, globals(), locals(), ['Weapon'], -1).Weapon
            costs += weaponClass.energyCost
        self.ui.lineEditReactor.setText(QtCore.QString(str(costs)+'/'+str(energy)))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    launcher = Main(packed)
    launcher.ui.show()
    sys.exit(app.exec_())

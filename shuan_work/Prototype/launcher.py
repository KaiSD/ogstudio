# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launcher.ui'
#
# Created: Sat Aug 14 23:31:38 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, uic
import sys, os, os.path
import game

class Main(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.ui = uic.loadUi('launcher.ui', baseinstance=None)
        
        #Connectors
        self.ui.pushButtonLaunch.clicked.connect(self.launch)
        self.ui.pushButtonAddWeapon.clicked.connect(self.addWeapon)
        self.ui.pushButtonRemoveWeapon.clicked.connect(self.removeWeapon)
        
        self.populateMissions()
        self.populateShips()
        self.populateGuns()
        self.populateWeapons()
        self.populateHeavyWeapons()
    
    def populateMissions(self):
        for i in os.listdir('Modules'):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.ui.comboBoxMission.addItem(QtCore.QString(i[:-3]))
    
    def populateShips(self):
        for i in os.listdir(os.path.join('Modules', 'Avatars')):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.ui.comboBoxShip.addItem(QtCore.QString(i[:-3]))
    
    def populateGuns(self):
        for i in os.listdir(os.path.join('Modules', 'Guns')):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.ui.comboBoxGun.addItem(QtCore.QString(i[:-3]))
    
    def populateWeapons(self):
        for i in os.listdir(os.path.join('Modules', 'Weapons')):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.ui.comboBoxWeapons.addItem(QtCore.QString(i[:-3]))
    
    def populateHeavyWeapons(self):
        for i in os.listdir(os.path.join('Modules', 'HeavyWeapons')):
            if i.endswith('.py') and not i.startswith('__init__'):
                self.ui.comboBoxHeavy.addItem(QtCore.QString(i[:-3]))
    
    def launch(self):
        mission = str(self.ui.comboBoxMission.currentText())
        ship = str(self.ui.comboBoxShip.currentText())
        heavy = str(self.ui.comboBoxHeavy.currentText())
        gun = str(self.ui.comboBoxGun.currentText())
        weapons = []
        for i in xrange(0, self.ui.listWidget.count()):
            weapons.append(str(self.ui.listWidget.takeItem(0).text()))
        self.ui.close()
        game.main(mission=mission, playerShip=ship, playerWeapons=weapons, playerGun=gun, playerHeavyWeapon=heavy)
    
    def addWeapon(self):
        weapon = self.ui.comboBoxWeapons.currentText()
        self.ui.listWidget.addItem(weapon)
    
    def removeWeapon(self):
        index = self.ui.listWidget.currentRow()
        self.ui.listWidget.takeItem(index)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    launcher = Main()
    launcher.ui.show()
    sys.exit(app.exec_())


#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype core module

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from ships import *

EXITDURATION = 6

'''
GAME MECHANICS CLASSES
'''
class Mission(layer.Layer):
    is_event_handler = True
    backgroundLayer = None
    
    def __init__(self):
        super(Mission, self).__init__()
        self.ready = True
        
        self.bounds = (20, director.get_window_size()[0]-20, 30, director.get_window_size()[1]-10)
        self.cursor = sprite.Sprite('data/graphics/target.png')
        self.avatar = None
        
        # Game Mechanics init
        self.schedule_interval(self.logic, 0.2)
        self.timer = 0
        self.lastTimerValue = 0
        self.score = 0
        self.target = None
        
        self.namedEnemies = {}
        self.meters = {}
        
        # Collisions
        self.schedule(self.frameUpdate)
        self.enemies = []
        self.avatarHelpers = []
        self.enemyBullets = []
        self.avatarBullets = []
        self.avatarRay = []
        self.enemyRay = []
        self.cmae = collision_model.CollisionManagerBruteForce()
        self.cmea = collision_model.CollisionManagerBruteForce()
        
        # Music and sounds
        self.soundList = []
        
        # HUD
        self.lifeLabel =  text.Label('connecting...',
                                font_name='Times New Roman',
                                font_size=16,
                                anchor_x='left', anchor_y='center')
        self.energyLaber =  text.Label('connecting...',
                                font_name='Times New Roman',
                                font_size=16,
                                anchor_x='left', anchor_y='center')
        self.scoreLabel =  text.Label('connecting...',
                                font_name='Times New Roman',
                                font_size=16,
                                anchor_x='left', anchor_y='center')
        self.lifeLabel.position = rel(0.1,0.1)
        self.energyLaber.position = rel(0.1,0.15)
        self.scoreLabel.position = rel(0.1,0.2)
        self.add(self.lifeLabel, z=10)
        self.add(self.energyLaber, z=10)
        self.add(self.scoreLabel, z=10)
        self.add(self.cursor, z=99)
    
    def setup(self):
        # Check if we need to reset the mission
        if self.ready == False:
            self.backgroundLayer = self.__class__.backgroundLayer
            self.reset()
        # Avatar setup
        self.avatar = Avatar(self, playerShips[Settings().avatarKind])
        self.avatar.setup(playerGuns, playerWeapons, playerDevices, playerShields, playerEngines, playerReactors)
        self.avatarHelpers.append(self.avatar)
        self.avatar.position = rel(0.5,0.5)
        self.add(self.avatar, z=6)
        self.ready = False
    
    def reset(self):
        self.__init__()
    
    def on_mouse_motion (self, x, y, dx, dy):
        bounds = self.bounds
        mouse = euclid.Vector2(x,y)
        apos = euclid.Vector2(self.avatar.position[0],self.avatar.position[1])
        dist = len(apos - mouse)
        self.cursor.position = x,y
        self.avatar.stop()
        self.avatar.do(actions.MoveTo((max(bounds[0],min(x,bounds[1])),
                                       max(bounds[2],min(y,bounds[3]))),
                                       duration=dist/self.avatar.engine))
    
    def on_mouse_press (self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            for w in self.avatar.weapons:
                if w.type == TURRET:
                    self.schedule_interval(self.autoAim, 0.5)
                    self.schedule_interval(self.shootTurret, w.pof, w)
                elif w.type == PROJECTILE:
                    self.shootBullet(0, w)
                    self.schedule_interval(self.shootBullet, w.pof, w)
                elif w.type == RAY:
                    self.shootLaser(w)
                if self.avatar.settings.sound:
                    if not w.startSound is None:
                        w.startSound.play()
                    if not w.loopSound is None:
                        if not w.loopSound in self.soundList:
                            w.loopSound.play(-1)
                            self.soundList.append(w.loopSound)
                self.avatar.consume += w.energy
        elif button == pyglet.window.mouse.RIGHT:
            pass
        self.on_mouse_drag(x, y, 0, 0, 0, 0)
    
    def on_mouse_release (self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            for w in self.avatar.weapons:
                if w.type == TURRET:
                    self.unschedule(self.autoAim)
                    self.unschedule(self.shootTurret)
                elif w.type == PROJECTILE:
                    self.unschedule(self.shootBullet)
                elif w.type == RAY:
                    self.stopLaser()
                elif w.type == EMPTY:
                    pass
                if self.avatar.settings.sound:
                    if not w.endSound is None:
                        w.endSound.play()
                    if not w.loopSound is None:
                        w.loopSound.stop()
                        if w.loopSound in self.soundList:
                            self.soundList.remove(w.loopSound)
                self.avatar.consume -= w.energy
        if button == pyglet.window.mouse.RIGHT:
            pass
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        bounds = self.bounds
        mouse = euclid.Vector2(x,y)
        apos = euclid.Vector2(self.avatar.position[0],self.avatar.position[1])
        dist = len(apos - mouse)
        self.cursor.position = x,y
        self.avatar.stop()
        self.avatar.do(actions.MoveTo((max(bounds[0],min(x,bounds[1])),
                                       max(bounds[2],min(y,bounds[3]))),
                                       duration=dist/self.avatar.engine))
        for ray in self.avatarRay:
            ray.stop()
            ray.timeScale = self.avatar.timeScale
            ray.do(actions.MoveTo((max(bounds[0]+ray.offset[0],min(x+ray.offset[0],bounds[1]+ray.offset[0])),
                                       max(bounds[2]+ray.offset[1],min(y+ray.offset[1],bounds[3]+ray.offset[1]))),
                                       duration=dist/self.avatar.engine))
    
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            stopAllSounds()
            stopMusic()
            self.missionAborted()
        return True
    
    def shootBullet(self, *args):
        Bullet(self.avatar, args[1], None)
    
    def shootTurret(self, *args):
        Bullet(self.avatar, args[1], self.target)
    
    def shootLaser(self, *args):
        Ray(self.avatar, args[0])
    
    def stopLaser(self, *args):
        for ray in self.avatarRay:
            ray.kill()
    
    def autoAim(self, *args):
        target = self.target
        enemies = self.enemies
        posX = self.avatar.position[0]
        posY = self.avatar.position[1]
        dist = 99999
        for i in enemies:
            ep = i.position
            if ep[1] > posY:
                d = abs(posX - ep[0])+abs(posY - ep[1])/3
                if d < dist:
                    target = i
                    dist = d
        self.target = target
    
    def addExplosion(self, pos, kind=0):
        def die(object):
            object.kill()
        explosion = sprite.Sprite(loadAnimation('data/graphics/basicExplosion.png', 9, 1, 0.05))
        explosion.position = pos
        self.add(explosion)
        explosion.do(actions.Delay(0.3) + actions.CallFuncS(die))
        sound = loadSound('data/sounds/explosion.wav', 0.7)
        if not sound is None:
            sound.play()
    
    def logic(self, *args):
        pass
    
    def missionFailed(self):
        self.stopGame()
        director.scene.endMission()
    
    def missionCompleted(self):
        self.stopGame()
        self.avatar.stop()
        self.is_event_handler = False
        self.avatar.do(actions.MoveBy((0,-100),1))
        director.scene.endMission()
        self.is_event_handler = True
    
    def missionAborted(self):
        self.stopGame()
        director.scene.endMission()
        self.backgroundLayer.do(actions.Delay(EXITDURATION) + ActionDie())
        self.do(actions.Delay(EXITDURATION) + ActionDie())
    
    def stopGame(self):
        stopMusic()
        
        for w in self.avatar.weapons:
            if w.type == TURRET:
                self.unschedule(self.autoAim)
                self.unschedule(self.shootTurret)
            elif w.type == PROJECTILE:
                self.unschedule(self.shootBullet)
            elif w.type == RAY:
                self.stopLaser()
            if self.avatar.settings.sound:
                if not w.endSound is None:
                    w.endSound.play()
                if not w.loopSound is None:
                    w.loopSound.stop()
                    if w.loopSound in self.soundList:
                        self.soundList.remove(w.loopSound)
        
        self.unschedule(self.logic)
        self.unschedule(self.frameUpdate)
        
        for i in self.enemies:
            i.disarm()
        
        
    
    def killAvatar(self):
        self.addExplosion(self.avatar.position)
        self.avatar.kill()
        label = text.Label('Rest in pieces! Your score is:%i' % (self.score),
                     font_name='Times New Roman',
                     font_size=32,
                     anchor_x='center', anchor_y='center')
        label.position = rel(0.5, 0.5)
        director.scene.add(label, z=4)
        self.missionFailed()
    
    def frameUpdate(self, *args):
        # Updating rays
        x = self.avatar.position[0]
        y = self.avatar.position[1]
        for ray in self.avatarRay:
            height = 600
            enemy = None
            for i in self.enemies:
                ep = i.position
                if abs(ep[0] - x - ray.offset[0]) <= i.width/2:
                    if ep[1] > y + ray.offset[1]:
                        h = ep[1] - y - ray.offset[1] + i.height/2
                        if h < height:
                            height = h
                            enemy = i
            ray.image.height = int(height)
            ray.do(actions.Show())
            if not enemy is None:
                if enemy.life > 0 and self.timer > self.lastTimerValue:
                    enemy.takeDamage(ray.damage)
                    self.lastTimerValue = self.timer
        for ray in self.enemyRay:
            if ray.owner in self.enemies:
                x = ray.owner.position[0]
                y = ray.owner.position[1]
                height = 600
                avatar = None
                for i in self.avatarHelpers:
                    ep = i.position
                    if abs(ep[0] - x) <= i.width + 8:
                        if y > ep[1]:
                            h = y - ep[1] + i.height / 3
                            if h < height:
                                height = h
                                avatar = i
                ray.image.height = int(height)
                ray.do(actions.Place((x,y)))
                if not avatar is None:
                    if avatar.life > 0 and self.timer > self.lastTimerValue:
                        avatar.takeDamage(ray.damage)
                        self.lastTimerValue = self.timer
            else:
                ray.kill()
        # Clearing collisions
        self.cmae.clear()
        self.cmea.clear()
        # Manage Avatar2Enemies Collision
        for bullet in self.avatarBullets:
            setCollision(bullet)
            self.cmae.add(bullet)
        for bullet in self.enemyBullets:
            setCollision(bullet)
            self.cmea.add(bullet)
        for enemy in self.enemies:
            setCollision(enemy)
            self.cmea.add(enemy)
            colls = self.cmae.objs_colliding(enemy)
            for i in colls:
                if i in self.avatarBullets:
                    i.kill()
                if enemy.life > 0:
                    enemy.takeDamage(i.damage)
        # Manage Enemies2Avatar Collision
        for avatar in self.avatarHelpers:
            setCollision(avatar)
            colls = self.cmea.objs_colliding(avatar)
            for i in colls:
                if avatar.life > 0:
                    avatar.takeDamage(i.damage)
                    sound = loadSound('data/sounds/hit.wav', 0.1)
                    if not sound is None:
                        sound.play()
                if i in self.enemies:
                    self.addExplosion(i.position)
                    if self.target == i:
                        self.target = None
                    if i.life > 0:
                        i.kill()
                elif i in self.enemyBullets:
                    i.kill()
        # Updating labels
        if self.avatar.shields > 0:
            self.lifeLabel.element.text = 'Armor (Shields): %i (%i)' % (self.avatar.hp, self.avatar.sp)
            if self.avatar.sp == 0:
                self.lifeLabel.element.color = (255, 255, 0, 255)
            else:
                self.lifeLabel.element.color = (255, 255, 255, 255)
        else:
            self.lifeLabel.element.text = 'Armor: %i' % (self.avatar.hp)
        
        self.energyLaber.element.text = 'Energy: %i%%' % (int(self.avatar.consume * 100 / self.avatar.reactor))
        if self.avatar.consume > self.avatar.reactor:
            self.energyLaber.element.color = (255, 255, 0, 255)
        else:
            self.energyLaber.element.color = (255, 255, 255, 255)
        
        self.scoreLabel.element.text = 'Score: %i' % (self.score)
        
        for e in self.namedEnemies.keys():
            self.meters[e].element.text = '%s: %i' % (e, self.namedEnemies[e].life)

class Game(scene.Scene):
    is_event_handler = True
    
    def __init__(self, *args):
        super(Game, self).__init__(*args)
        self.returnScene = director.scene
        self.mission = None
        for i in args:
            if issubclass(i.__class__, Mission):
                self.mission = i
        self.mission.backgroundLayer = args[0]
        director.window.set_mouse_visible(False)
    
    def endMission(self):
        director.replace(scenes.FadeTransition(self.returnScene, duration=EXITDURATION))
        director.window.set_mouse_visible(True)
        self.do(actions.Delay(EXITDURATION) + ActionDie())
    
    def setTimeScale(self, ts):
        pass
    
    def resetTimeScale(self):
        pass
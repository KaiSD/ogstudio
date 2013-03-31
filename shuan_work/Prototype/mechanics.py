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
        
        # Game Mechanics init
        self.timer = 0
        self.lastTimerValue = 0
        self.score = 0
        self.target = None
        self.schedule_interval(self.logic, 0.2)
        self.schedule_interval(self.autoAim, 0.5)
        
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
        self.devicesLabel =  text.Label('[connecting...',
                                font_name='Times New Roman',
                                font_size=16,
                                anchor_x='center', anchor_y='bottom')
        self.lifeLabel.position = rel(0.1,0.1)
        self.energyLaber.position = rel(0.1,0.15)
        self.scoreLabel.position = rel(0.1,0.2)
        self.devicesLabel.position = rel(0.5,0.95)
        self.add(self.lifeLabel, z=10)
        self.add(self.energyLaber, z=10)
        self.add(self.scoreLabel, z=10)
        self.add(self.devicesLabel, z=10)
        self.add(self.cursor, z=99)
    
    def setup(self):
        # Check if we need to reset the mission
        if self.ready == False:
            self.backgroundLayer = self.__class__.backgroundLayer
            self.reset()
        # Avatar setup
        avatar = Avatar(self, playerShips[Settings().avatarKind])
        avatar.setup(playerGuns, playerWeapons, playerDevices, playerShields, playerEngines, playerReactors)
        self.avatarHelpers.append(avatar)
        avatar.position = rel(0.5,0.5)
        self.add(avatar, z=6)
        currents['layerObject'] = self
        currents['avatarObject'] = avatar
        self.ready = False
    
    def reset(self):
        self.__init__()
    
    def on_mouse_motion (self, x, y, dx, dy):
        bounds = self.bounds
        mouse = euclid.Vector2(x,y)
        apos = euclid.Vector2(currents['avatarObject'].position[0],currents['avatarObject'].position[1])
        dist = len(apos - mouse)
        self.cursor.position = x,y
        currents['avatarObject'].stop()
        currents['avatarObject'].do(actions.MoveTo((max(bounds[0],min(x,bounds[1])),
                                       max(bounds[2],min(y,bounds[3]))),
                                       duration=dist/currents['avatarObject'].engine))
    
    def on_mouse_press (self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            for w in currents['avatarObject'].weapons:
                if w.infinite or w.ammo > 0:
                    if w.type == TURRET:
                        self.schedule_interval(self.shootTurret, w.pof, w)
                    elif w.type == PROJECTILE:
                        self.shootBullet(0, w)
                        self.schedule_interval(self.shootBullet, w.pof, w)
                    elif w.type == RAY:
                        self.shootLaser(w)
                    if currents['avatarObject'].settings.sound:
                        if not w.startSound is None:
                            w.startSound.play()
                        if not w.loopSound is None:
                            if not w.loopSound in self.soundList:
                                w.loopSound.play(-1)
                                self.soundList.append(w.loopSound)
                currents['avatarObject'].consume += w.energy
        elif button == pyglet.window.mouse.RIGHT:
            pass
        self.on_mouse_drag(x, y, 0, 0, 0, 0)
    
    def on_mouse_release (self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            for w in currents['avatarObject'].weapons:
                if w.type == TURRET:
                    self.unschedule(self.shootTurret)
                elif w.type == PROJECTILE:
                    self.unschedule(self.shootBullet)
                elif w.type == RAY:
                    self.stopLaser()
                elif w.type == EMPTY:
                    pass
                if currents['avatarObject'].settings.sound:
                    if not w.endSound is None:
                        w.endSound.play()
                    if not w.loopSound is None:
                        w.loopSound.stop()
                        if w.loopSound in self.soundList:
                            self.soundList.remove(w.loopSound)
                currents['avatarObject'].consume -= w.energy
        if button == pyglet.window.mouse.RIGHT:
            pass
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        bounds = self.bounds
        mouse = euclid.Vector2(x,y)
        apos = euclid.Vector2(currents['avatarObject'].position[0],currents['avatarObject'].position[1])
        dist = len(apos - mouse)
        self.cursor.position = x,y
        currents['avatarObject'].stop()
        currents['avatarObject'].do(actions.MoveTo((max(bounds[0],min(x,bounds[1])),
                                       max(bounds[2],min(y,bounds[3]))),
                                       duration=dist/currents['avatarObject'].engine))
        for ray in self.avatarRay:
            ray.stop()
            ray.timeScale = currents['avatarObject'].timeScale
            ray.do(actions.MoveTo((max(bounds[0]+ray.offset[0],min(x+ray.offset[0],bounds[1]+ray.offset[0])),
                                       max(bounds[2]+ray.offset[1],min(y+ray.offset[1],bounds[3]+ray.offset[1]))),
                                       duration=dist/currents['avatarObject'].engine))
    
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            stopAllSounds()
            stopMusic()
            self.missionAborted()
        elif symbol == pyglet.window.key._1:
            if len(currents['avatarObject'].devices) > 0:
                w = currents['avatarObject'].devices[0]
                if w.type == EFFECT:
                    if w.infinite or w.ammo > 0:
                        EffectRunner(w.runner, currents['avatarObject'])
                        w.ammo -= 1
                if w.type == TURRET:
                    self.shootTurret(0, w)
                if w.type == PROJECTILE:
                    self.shootBullet(0, w)
                if w.type == SPAWN:
                    if w.infinite or w.ammo > 0:
                        pos = abs2rel(*currents['avatarObject'].position)
                        free = shipsFree.get(helpers[w.spawnID],[])
                        if free:
                            free[0].reinstate(pos[0], pos[1])
                        else:
                            Helper(self, helpers[w.spawnID], pos[0], pos[1])
                        w.ammo -= 1
        elif symbol == pyglet.window.key._2:
            if len(currents['avatarObject'].devices) > 1:
                w = currents['avatarObject'].devices[1]
                if w.type == EFFECT:
                    if w.infinite or w.ammo > 0:
                        EffectRunner(w.runner, currents['avatarObject'])
                        w.ammo -= 1
                if w.type == TURRET:
                    self.shootTurret(0, w)
                if w.type == PROJECTILE:
                    self.shootBullet(0, w)
                if w.type == SPAWN:
                    if w.infinite or w.ammo > 0:
                        pos = abs2rel(*currents['avatarObject'].position)
                        free = shipsFree.get(helpers[w.spawnID],[])
                        if free:
                            free[0].reinstate(pos[0], pos[1])
                        else:
                            Helper(self, helpers[w.spawnID], pos[0], pos[1])
                        w.ammo -= 1
        elif symbol == pyglet.window.key._3:
            if len(currents['avatarObject'].devices) > 2:
                w = currents['avatarObject'].devices[2]
                if w.type == EFFECT:
                    if w.infinite or w.ammo > 0:
                        EffectRunner(w.runner, currents['avatarObject'])
                        w.ammo -= 1
                if w.type == TURRET:
                    self.shootTurret(0, w)
                if w.type == PROJECTILE:
                    self.shootBullet(0, w)
                if w.type == SPAWN:
                    if w.infinite or w.ammo > 0:
                        pos = abs2rel(*currents['avatarObject'].position)
                        free = shipsFree.get(helpers[w.spawnID],[])
                        if free:
                            free[0].reinstate(pos[0], pos[1])
                        else:
                            Helper(self, helpers[w.spawnID], pos[0], pos[1])
                        w.ammo -= 1
        return True
    
    def shootBullet(self, timer, weapon):
        free = bulletsFree.get(weapon, []) 
        avatar = currents['avatarObject']
        if weapon.infinite or weapon.ammo > 0:
            if weapon.directions > 1:
                if not weapon.oneByOne:
                    for i in xrange(0, weapon.directions):
                        if free:
                            free[0].reinstate(avatar, None, weapon.angle + (2.0 * i / (weapon.directions - 1) - 1) * weapon.spread)
                        else:
                            Bullet(avatar, weapon, None, weapon.angle + (2.0 * i / (weapon.directions - 1) - 1) * weapon.spread)
                else:
                    i = weapon.tick % weapon.directions
                    angle = (weapon.angle + (2.0 * i / (weapon.directions - 1) - 1) * weapon.spread) * weapon.amod
                    if free:
                        free[0].reinstate(avatar, None, angle)
                    else:
                        Bullet(avatar, weapon, None, angle)
                    weapon.tick += 1
            else:
                if free:
                    free[0].reinstate(avatar, None, weapon.angle * weapon.amod)
                else:
                    Bullet(avatar, weapon, None, weapon.angle * weapon.amod)
            weapon.ammo -= 1
    
    def shootTurret(self, timer, weapon):
        free = bulletsFree.get(weapon, []) 
        avatar = currents['avatarObject']
        if weapon.infinite or weapon.ammo > 0:
            if free:
                free[0].reinstate(avatar, self.target)
            else:
                Bullet(currents['avatarObject'], weapon, self.target)
            weapon.ammo -= 1
    
    def shootLaser(self, weapon):
        Ray(currents['avatarObject'], weapon)
        weapon.ammo -= 1
    
    def stopLaser(self, *args):
        for ray in self.avatarRay:
            ray.kill()
    
    def autoAim(self, *args):
        target = self.target
        enemies = self.enemies
        posX = currents['avatarObject'].position[0]
        posY = currents['avatarObject'].position[1]
        dist = 99999
        for i in enemies:
            ep = i.position
            if ep[1] > posY:
                d = abs(posX - ep[0])+abs(posY - ep[1])/3
                if d < dist:
                    target = i
                    dist = d
        self.target = target
        for h in self.avatarHelpers:
            h.target = target
    
    def addExplosion(self, pos, kind=0):
        def die(object):
            object.kill()
        explosion = sprite.Sprite(loadAnimation('data/graphics/basicExplosion.png', 9, 1, 0.05))
        explosion.position = pos
        self.add(explosion)
        explosion.do(adata['aDelay03'] + actions.CallFuncS(die))
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
        currents['avatarObject'].stop()
        self.is_event_handler = False
        currents['avatarObject'].do(actions.MoveBy((0,-100),1))
        director.scene.endMission()
        self.is_event_handler = True
    
    def missionAborted(self):
        self.stopGame()
        director.scene.endMission()
        self.backgroundLayer.do(actions.Delay(EXITDURATION) + adata['aDie'])
        self.do(actions.Delay(EXITDURATION) + adata['aDie'])
    
    def stopGame(self):
        stopMusic()
        
        for w in currents['avatarObject'].weapons:
            if w.type == TURRET:
                self.unschedule(self.autoAim)
                self.unschedule(self.shootTurret)
            elif w.type == PROJECTILE:
                self.unschedule(self.shootBullet)
            elif w.type == RAY:
                self.stopLaser()
            if currents['avatarObject'].settings.sound:
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
        self.addExplosion(currents['avatarObject'].position)
        currents['avatarObject'].kill()
        label = text.Label('Rest in pieces! Your score is:%i' % (self.score),
                     font_name='Times New Roman',
                     font_size=32,
                     anchor_x='center', anchor_y='center')
        label.position = rel(0.5, 0.5)
        director.scene.add(label, z=4)
        self.missionFailed()
    
    def frameUpdate(self, *args):
        avatar = currents['avatarObject'] 
        # Updating rays
        x = avatar.position[0]
        y = avatar.position[1]
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
                if enemy.takenDamage > enemy.life and self.timer > self.lastTimerValue:
                    enemy.takeDamage(ray.damage)
                    self.lastTimerValue = self.timer
        for ray in self.enemyRay:
            if ray.owner in self.enemies:
                x = ray.owner.position[0]
                y = ray.owner.position[1]
                height = 600
                av = None
                for i in self.avatarHelpers:
                    ep = i.position
                    if abs(ep[0] - x) <= i.width + 8:
                        if y > ep[1]:
                            h = y - ep[1] + i.height / 3
                            if h < height:
                                height = h
                                av = i
                ray.image.height = int(height)
                ray.do(actions.Place((x,y)))
                if not av is None:
                    if av.takenDamage < av.life and self.timer > self.lastTimerValue:
                        av.takeDamage(ray.damage)
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
        for av in self.avatarHelpers:
            setCollision(av)
            colls = self.cmea.objs_colliding(av)
            for i in colls:
                if av.life > 0:
                    av.takeDamage(i.damage)
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
        if avatar.shields > 0:
            self.lifeLabel.element.text = 'Armor (Shields): %i (%i)' % (avatar.hp, avatar.sp)
            if avatar.sp == 0:
                self.lifeLabel.element.color = (255, 255, 0, 255)
            else:
                self.lifeLabel.element.color = (255, 255, 255, 255)
        else:
            self.lifeLabel.element.text = 'Armor: %i' % (avatar.hp)
        
        self.energyLaber.element.text = 'Energy: %i%%' % (int(avatar.consume * 100 / avatar.reactor))
        if avatar.consume > avatar.reactor:
            self.energyLaber.element.color = (255, 255, 0, 255)
        else:
            self.energyLaber.element.color = (255, 255, 255, 255)
        
        self.scoreLabel.element.text = 'Score: %i' % (self.score)
        
        for e in self.namedEnemies.keys():
            ship = self.namedEnemies[e]
            self.meters[e].element.text = '%s: %i' % (e, ship.life - ship.takenDamage)
        
        devices = avatar.devices
        dlist = (devices[0].name, devices[0].ammo, devices[1].name, devices[1].ammo, devices[2].name, devices[2].ammo)
        self.devicesLabel.element.text = '1:[%s-%i] 2:[%s-%i] 3:[%s-%i]' % dlist

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
        self.do(actions.Delay(EXITDURATION) + adata['aDie'])
    
    def setTimeScale(self, ts):
        pass
    
    def resetTimeScale(self):
        pass
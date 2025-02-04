"""
Player (movement) controller
"""

import pymjin2

class MovementController(pymjin2.InputListener):
    def __init__(self):
        pymjin2.InputListener.__init__(self)
        self.player = None
        self.speed = 5
    def onInput(self, e):
        if (self.player and e.press):
            pos = self.player.position()
            rot = pymjin2.Vec3()
            # Position.
            if (e.input == pymjin2.INPUT_KEY_UP):
                pos.y += self.speed
            elif (e.input == pymjin2.INPUT_KEY_DOWN):
                pos.y -= self.speed
            elif (e.input == pymjin2.INPUT_KEY_LEFT):
                pos.x -= self.speed
            elif (e.input == pymjin2.INPUT_KEY_RIGHT):
                pos.x += self.speed
            elif (e.input == pymjin2.INPUT_KEY_PAGE_DOWN):
                pos.z -= self.speed
            elif (e.input == pymjin2.INPUT_KEY_PAGE_UP):
                pos.z += self.speed
            # Rotation.
            elif (e.input == pymjin2.INPUT_KEY_A):
                rot.z += self.speed
            elif (e.input == pymjin2.INPUT_KEY_D):
                rot.z -= self.speed
            elif (e.input == pymjin2.INPUT_KEY_W):
                rot.x -= self.speed
            elif (e.input == pymjin2.INPUT_KEY_S):
                rot.x += self.speed
            else:
                return
            print "Moving to ({0}, {1}, {2})".format(pos.x, pos.y, pos.z)
            self.player.setPosition(pos)
            print "Rotating ({0}, {1}, {2})".format(rot.x, rot.y, rot.z)
            self.player.setRotation(
                pymjin2.rotationSum(self.player.rotation(),
                                    pymjin2.degreeToQuaternion(rot)))
    def setPlayer(self, player):
        self.player = player
        # Not sure if this is necessary, but let it be.
        if (self.player):
            self.player.setPosition(self.player.position())
            self.player.setRotation(self.player.rotation())

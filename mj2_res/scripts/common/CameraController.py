"""
Camera controller
"""

import pymjin2

class CameraController(pymjin2.InputListener):
    def __init__(self):
        pymjin2.InputListener.__init__(self)
        self.camera = None
        self.rotation = pymjin2.Vec3(90, 0, 0)
        self.x = None
        self.y = None
        self.speed = 0.5
    def onInput(self, e):
        if (self.x == None and self.y == None):
            self.x = e.x
            self.y = e.y
        elif (self.camera and e.press and e.input == pymjin2.INPUT_MOUSE_MOVE):
            dx = e.x - self.x
            dy = e.y - self.y
            dx *= self.speed
            dy *= self.speed
            print "dx: {0} dy : {1}".format(dx, dy)
            self.rotation.z -= dx
            self.rotation.x -= dy
            print "rotation: {0} {1} {2}".format(self.rotation.x, self.rotation.y, self.rotation.z)
            self.camera.setRotation(pymjin2.degreeToQuaternion(self.rotation))
            self.x = e.x
            self.y = e.y
    def setCamera(self, camera):
        self.camera = camera

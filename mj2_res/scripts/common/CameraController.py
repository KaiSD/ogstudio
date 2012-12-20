"""
Camera controller
"""

import pymjin2

class CameraController(pymjin2.InputListener):
    def __init__(self):
        pymjin2.InputListener.__init__(self)
        self.camera = None
        self.rotation = pymjin2.Vec3(90, 0, 0)
        self.x = 0
        self.y = 0
        self.speed = 0.5
    def onInput(self, e):
        if (self.camera and e.press and e.input == pymjin2.INPUT_MOUSE_MOVE):
            dx = e.x - self.x
            dy = e.y - self.y
            dx *= self.speed
            dy *= self.speed
            self.rotation.x += dx
            self.rotation.y += dy
            self.camera.setRotation(pymjin2.degreeToQuaternion(self.rotation))
            self.x = e.x
            self.y = e.y
    def setCamera(self, camera):
        self.camera = camera

"""
Camera controller
"""

import pymjin2

class CameraController(pymjin2.InputListener):
    def __init__(self):
        pymjin2.InputListener.__init__(self)
        self.camera = None
        self.x = None
        self.y = None
        self.speed = 0.1
        self.canMove = False
    def onInput(self, e):
        if (self.camera and e.input == pymjin2.INPUT_MOUSE_BUTTON_RIGHT):
            self.canMove = e.press
            # Reset x, y.
            if (self.x == None and self.y == None):
                self.x = e.x
                self.y = e.y
        elif (self.canMove and e.input == pymjin2.INPUT_MOUSE_MOVE):
            dx = e.x - self.x
            dy = e.y - self.y
            dx *= self.speed
            dy *= self.speed
            self.camera.setRotation(
                pymjin2.rotationSum(self.camera.rotation(),
                            pymjin2.degreeToQuaternion(pymjin2.Vec3(-dy, -dx, 0))))
                                        
            self.x = e.x
            self.y = e.y
    def setCamera(self, camera):
        self.camera = camera
        if (self.camera):
            self.camera.setRotation(self.camera.rotation())

"""
Camera controller
"""

import mjin2

class CameraController(mjin2.InputListener):
    def __init__(self, camera):
        mjin2.InputListener.__init__(self)
        self.camera = camera
        self.rotation = mjin2.Vec3(90, 0, 0)
        self.x = 0
        self.y = 0
    def onInput(self, e):
        if (e.press and e.input == mjin2.INPUT_MOUSE_MOVE):
            dx = e.x - self.x
            dy = e.y - self.y
            self.rotation.x += dx
            self.rotation.y += dy
            self.camera.setRotation(self.rotation)
            self.x = e.x
            self.y = e.y

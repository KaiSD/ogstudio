"""
Game (action) controller
"""

import pymjin2

class ActionController(pymjin2.InputListener):
    def __init__(self):
        pymjin2.InputListener.__init__(self)
        self.sceneNodeSelector = pymjin2.SceneNodeSelector()
    def __del__(self):
        del self.sceneNodeSelector
    def onInput(self, e):
        if (self.sceneNodeSelector and
            e.input == pymjin2.INPUT_MOUSE_BUTTON_LEFT and
            e.press):
            n = self.sceneNodeSelector.select(e.x, e.yi)
            if (n):
                print "Selected node: {0}".format(n.name())
            else:
                print "No valid node selected"
    def setCamera(self, cam):
        self.sceneNodeSelector.setCamera(cam)

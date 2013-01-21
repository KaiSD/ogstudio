"""
Game (action) controller
"""

import pymjin2

class ActionController(pymjin2.InputListener):
    def __init__(self):
        pymjin2.InputListener.__init__(self)
        self.sceneNodeSelector = None
    def __del__(self):
        if (self.sceneNodeSelector):
            del self.sceneNodeSelector
    def onInput(self, e):
        if (not self.sceneNodeSelector):
            return
        if (e.input != pymjin2.MOUSE_BUTTON_LEFT):
            return
        n = self.sceneNodeSelector.select(e.x, e.yi)
        if (n):
            print "Selected node: {0}".format(n.name())
        else:
            print "No valid node selected"
    def setCamera(self, cam):
        self.sceneNodeSelector = pymjin2.SceneNodeSelector(cam)

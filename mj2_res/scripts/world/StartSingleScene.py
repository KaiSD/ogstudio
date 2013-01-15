
from CameraController import *

def run(listener):
    print "Scenes in the World: {0}".format(len(listener.parent.scenes))
    world = listener.parent
    if (len(world.scenes) == 1):
        print "There's only one Scene found in the World. Starting it."
        sceneName = world.scenes.keys()[0]
        print "Scene to start: {0}".format(sceneName)
        world.startScene(sceneName)
        scene = world.scenes[sceneName]
        player = world.player
        player.setScene(scene.scene)
        player.setSceneCamera(scene.scene.child("MainPlayer").child("MainCamera"))
        cc = CameraController()
        player.setSceneCameraController(cc)


import pymjin2
#from ActionController import *
from CameraController import *
from MovementController import *

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
        # Scene player.
        scenePlayer = pymjin2.castSceneNodeToScenePlayer(
            scene.scene.child("MainPlayer"))
        player.setScenePlayer(scenePlayer)
        mc = MovementController()
        player.setScenePlayerController(mc)
        # Scene camera.
        player.setSceneCamera(pymjin2.castSceneNodeToSceneCamera(
            scenePlayer.child("MainCamera")))
        cc = CameraController()
        player.setSceneCameraController(cc)
        # Action controller.
        #ac = ActionController()
        #player.setActionController(ac)


def run(listener):
    world = listener.parent
    if (len(world.scenes) == 1):
        print "There's only one Scene found in the World. Finishing it."
        world.finishScene(world.scenes.keys()[0])
        world.player.setScene(None)
        world.player.setSceneCamera(None)
        world.player.setSceneCameraController(None)
        world.player.setScenePlayer(None)
        world.player.setScenePlayerController(None)


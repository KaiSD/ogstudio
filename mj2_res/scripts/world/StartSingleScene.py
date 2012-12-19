
def run(listener):
    print "Scenes in the World: {0}".format(len(listener.parent.scenes))
    world = listener.parent
    if (len(world.scenes) == 1):
        print "There's only one Scene found in the World. Starting it."
        sceneName = world.scenes.keys()[0]
        print "Scene to start: {0}".format(sceneName)
        world.startScene(sceneName)
        scene = world.scenes[sceneName]
        world.player.setScene(scene.scene)
        world.player.setActiveCamera(scene.scene.camera("main"))


def run(listener):
    print "Scenes in the World: {0}".format(len(listener.parent.scenes))
    world = listener.parent
    if (len(world.scenes) == 1):
        print "There's only one Scene found in the World. Starting it."
        print "Scene to start: {0}".format(world.scenes.keys()[0])
        world.startScene(world.scenes.keys()[0])

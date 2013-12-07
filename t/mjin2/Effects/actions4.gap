moveConveyorBelt
    type=move
    points
        position=0 10 0
        duration=0
        position=22 10 0
        duration=5000
    reversed=0
    node=box1
placeBox
    type=move
    instant=1
    points
        position=0 0 150
        position=30 7 10
removeBox
    type=move
    instant=1
    points
        position=-8 7 10
        position=0 0 150
robot1A
    type=move
    points
        position=-30 10 150
        position=-30 10 0
        duration=5000
robot1Back
    type=move
    template=robot1A
    reversed=1
robot2A
    type=move
    points
    position=-8 10 150
        position=-8 10 0
        duration=5000
robot2ABack
    type=move
    template=robot2A
    reversed=1
robot3A
    type=move
    points
        position=14 10 150
        position=14 10 0
        duration=5000
robot3ABack
    type=move
    template=robot3A
    reversed=1
moveBox
    type=moveBy
    points
        position=22 0 0
    points
        duration=5000
    nodes=box2
movePlane
    type=moveBy
    template=moveBox
upliftConveyor
    type=moveTo
    template=
    instant=0
    interpolation=linear
    points
        position=0 10 0
        duration=1000
    node=box3
forward
    type=sequence
    actions=moveBelt
    actions=robot1A
    actions=placeBox
    actions=robot1ABack
    actions=moveBoxAndBelt
    actions=robot2A
    actions=removeBox
    actions=reobot2ABack
    actions=movePlaneAndBelt
    actions=robot3A
    actions=robot3ABack
moveBoxAndBelt
    type=spawn
    actions=moveBox
    actions=moveBelt
movePlaneAndBelt
    type=spawn
    actions=movePlane
    actions=moveBelt

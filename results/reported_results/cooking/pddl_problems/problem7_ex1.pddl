(define (problem cooking7)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    cucumber - veggie
    tomato - veggie
    carrot - veggie
)
(:init
    ( at bowl black_tray )
    ( at carrot black_tray )
    ( at cucumber black_tray )
    ( at tomato black_tray )
    ( available bowl )
    ( available carrot )
    ( available cucumber )
    ( available tomato )
    ( carry robotic_gripper chopping_knife )
    ( free robotic_gripper1 )
    ( is-whole carrot )
    ( is-whole cucumber )
    ( is-whole tomato )
)

(:goal
    (and
        (in cucumber bowl)
        (in carrot bowl)
        (in tomato bowl)
        (is-sliced cucumber)
        (is-sliced carrot)
        (is-sliced tomato)
    )
)
)

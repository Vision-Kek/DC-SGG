(define (problem cooking6)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    cucumber - veggie
    carrot - veggie
)
(:init
    ( at bowl black_tray )
    ( at carrot black_tray )
    ( at cucumber black_tray )
    ( available bowl )
    ( available carrot )
    ( available cucumber )
    ( carry robotic_gripper chopping_knife )
    ( free robotic_gripper1 )
    ( is-whole carrot )
    ( is-whole cucumber )
)

    (:goal
        (and
            (in cucumber bowl)
            (in carrot bowl)
            (is-sliced cucumber)
            (is-sliced carrot)
        )
    )
)

(define (problem cooking4)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    tomato - veggie
    carrot - veggie
)
(:init
    ( at bowl black_tray )
    ( at carrot black_tray )
    ( at tomato black_tray )
    ( available bowl )
    ( available carrot )
    ( available tomato )
    ( carry robotic_gripper1 chopping_knife )
    ( free robotic_gripper )
    ( is-whole carrot )
    ( is-whole tomato )
)

    (:goal
        (and
            (in carrot bowl)
            (in tomato bowl)
            (is-sliced carrot)
            (is-sliced tomato)
        )
    )
)

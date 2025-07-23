(define (problem cooking2)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    chopping_knife - cuttool
    tomato - veggie
)
(:init
    ( at bowl black_tray )
    ( at tomato black_tray )
    ( available bowl )
    ( available tomato )
    ( carry robotic_gripper chopping_knife )
    ( is-sliced tomato )
)

    (:goal
        (and
            (in tomato bowl)
            (is-sliced tomato)
        )
    )
)

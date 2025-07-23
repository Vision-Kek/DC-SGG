(define (problem cooking10)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    tomato - veggie
    vegetable1 - veggie
    vegetable2 - veggie
)
(:init
    ( at bowl black_tray )
    ( at tomato black_tray )
    ( at vegetable1 wooden_board )
    ( at vegetable2 wooden_board )
    ( available bowl )
    ( available tomato )
    ( carry robotic_gripper vegetable2 )
    ( carry robotic_gripper1 chopping_knife )
    ( carry robotic_gripper1 vegetable1 )
    ( carry robotic_gripper1 vegetable2 )
    ( is-whole tomato )
    ( is-whole vegetable1 )
    ( is-whole vegetable2 )
)

    (:goal
        (and
            (in tomato bowl)
            (is-sliced tomato)
        )
    )
)

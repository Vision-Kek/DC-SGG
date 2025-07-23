(define (problem cooking3)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    carrot - veggie
)
(:init
    ( at bowl black_tray )
    ( at carrot black_tray )
    ( available bowl )
    ( available carrot )
    ( carry robotic_gripper1 chopping_knife )
    ( free robotic_gripper )
    ( is-whole carrot )
)

    (:goal
        (and
            (in carrot bowl)
            (is-sliced carrot)
        )
    )
)

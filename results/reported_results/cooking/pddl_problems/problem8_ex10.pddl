(define (problem cooking8)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    cucumber - veggie
    vegetable1 - veggie
    vegetable2 - veggie
)
(:init
    ( at bowl black_tray )
    ( at cucumber black_tray )
    ( at vegetable1 wooden_board )
    ( at vegetable2 wooden_board )
    ( available bowl )
    ( available cucumber )
    ( available vegetable1 )
    ( available vegetable2 )
    ( carry robotic_gripper1 chopping_knife )
    ( free robotic_gripper )
    ( is-sliced vegetable1 )
    ( is-sliced vegetable2 )
    ( is-whole cucumber )
)

    (:goal
        (and
            (in cucumber bowl)
            (is-sliced cucumber)
        )
    )
)

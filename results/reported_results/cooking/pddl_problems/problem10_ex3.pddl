(define (problem cooking10)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    vegetable - veggie
    vegetable1 - veggie
    vegetable2 - veggie
)
(:init
    ( at bowl black_tray )
    ( at vegetable black_tray )
    ( at vegetable1 wooden_board )
    ( at vegetable2 wooden_board )
    ( available bowl )
    ( available vegetable )
    ( carry robotic_gripper vegetable2 )
    ( carry robotic_gripper1 chopping_knife )
    ( carry robotic_gripper1 vegetable1 )
    ( carry robotic_gripper1 vegetable2 )
    ( is-whole vegetable )
    ( is-whole vegetable1 )
    ( is-whole vegetable2 )
)

    (:goal
        (and
            (forall (?v - veggie) (in ?v bowl) )
            (forall (?v - veggie) (is-sliced ?v) )
        )
    )
)

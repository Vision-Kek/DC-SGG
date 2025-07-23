(define (problem cooking9)
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
    ( at vegetable wooden_board )
    ( at vegetable1 wooden_board )
    ( at vegetable2 black_tray )
    ( available bowl )
    ( available vegetable )
    ( available vegetable1 )
    ( available vegetable2 )
    ( carry robotic_gripper1 chopping_knife )
    ( free robotic_gripper )
    ( is-sliced vegetable )
    ( is-sliced vegetable1 )
    ( is-whole vegetable2 )
)

    (:goal
        (and
            (forall (?v - veggie) (in ?v bowl) )
            (forall (?v - veggie) (is-sliced ?v) )
        )
    )
)

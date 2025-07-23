(define (problem cooking6)
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
)
(:init
    ( at bowl black_tray )
    ( at vegetable black_tray )
    ( at vegetable1 black_tray )
    ( available bowl )
    ( available vegetable )
    ( available vegetable1 )
    ( carry robotic_gripper chopping_knife )
    ( free robotic_gripper1 )
    ( is-whole vegetable )
    ( is-whole vegetable1 )
)

(:goal
    (and
        (forall (?v - veggie) (in ?v bowl) )
        (forall (?v - veggie) (is-sliced ?v) )
    )
)
)

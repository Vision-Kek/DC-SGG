(define (problem cooking1)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    vegetable - veggie
)
(:init
    ( at bowl black_tray )
    ( at vegetable black_tray )
    ( available bowl )
    ( available vegetable )
    ( carry robotic_gripper1 chopping_knife )
    ( free robotic_gripper )
    ( is-whole vegetable )
)

    (:goal
        (and
            (forall (?v - veggie) (in ?v bowl) )
            (forall (?v - veggie) (is-sliced ?v) )
        )
    )
)

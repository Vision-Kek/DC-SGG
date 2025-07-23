(define (problem cooking5)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    cucumber - veggie
    tomato - veggie
)
(:init
    ( at bowl black_tray )
    ( at cucumber black_tray )
    ( at tomato black_tray )
    ( available bowl )
    ( available cucumber )
    ( available tomato )
    ( carry robotic_gripper chopping_knife )
    ( free robotic_gripper1 )
    ( is-whole cucumber )
    ( is-whole tomato )
)

    (:goal
        (and
            (forall (?v - veggie) (in ?v bowl) )
            (is-sliced cucumber)
            (is-sliced tomato)
        )
    )
)

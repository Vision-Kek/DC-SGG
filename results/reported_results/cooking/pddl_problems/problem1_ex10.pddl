(define (problem cooking1)
(:domain cooking)
(:objects
    black_tray - location
    wooden_board - workspace
    bowl - container
    robotic_gripper - gripper
    robotic_gripper1 - gripper
    chopping_knife - cuttool
    cucumber - veggie
)
(:init
    ( at bowl black_tray )
    ( at cucumber black_tray )
    ( available bowl )
    ( available cucumber )
    ( carry robotic_gripper1 chopping_knife )
    ( free robotic_gripper )
    ( is-whole cucumber )
)

    (:goal
        (and
            (in cucumber bowl)
            (is-sliced cucumber)
        )
    )
)

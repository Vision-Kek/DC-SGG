(define (problem cooking1)
    (:domain cooking)
    (:objects
        cucumber - veggie
        counter - location
        cutting_board - workspace
        bowl - container
        a_bot b_bot - gripper
        knife - cuttool
    )
    (:init
        (free a_bot)
        (carry b_bot knife)
        (at bowl counter)
        (available cucumber)
        (is-whole cucumber)
        (at cucumber counter)
    )
    (:goal
        (and
            (forall (?v - veggie) (in ?v bowl) )
            (forall (?v - veggie) (is-sliced ?v) )
        )
    )
)

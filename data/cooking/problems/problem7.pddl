(define (problem cooking7)
    (:domain cooking)
    (:objects
        cucumber carrot tomato - veggie
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
        (available carrot)
        (is-whole carrot)
        (at carrot counter)
        (available tomato)
        (is-whole tomato)
        (at tomato counter)
    )
    (:goal
        (and
            (forall (?v - veggie) (in ?v bowl) )
            (forall (?v - veggie) (is-sliced ?v) )
        )
    )
)

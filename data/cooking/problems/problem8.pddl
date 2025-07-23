(define (problem cooking8)
    (:domain cooking)
    (:objects
        cucumber tomato1 tomato2 - veggie
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
        (available tomato1)
        (at tomato1 cutting_board)
        (available tomato2)
        (at tomato2 cutting_board)
        (is-sliced tomato1)
        (is-sliced tomato2)
    )
    (:goal
        (and
            (forall (?v - veggie) (in ?v bowl) )
            (forall (?v - veggie) (is-sliced ?v) )
        )
    )
)

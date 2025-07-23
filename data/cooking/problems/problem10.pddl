(define (problem cooking10)
    (:domain cooking)
    (:objects
        carrot1 carrot2 tomato - veggie
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
        (available carrot1)
        (at carrot1 cutting_board)
        (available carrot2)
        (at carrot2 cutting_board)
        (available tomato)
        (is-whole tomato)
        (at tomato counter)
        (is-sliced carrot1)
        (is-sliced carrot2)
    )
    (:goal
        (and
            (forall (?v - veggie) (in ?v bowl) )
            (forall (?v - veggie) (is-sliced ?v) )
        )
    )
)

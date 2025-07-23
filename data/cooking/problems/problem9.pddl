(define (problem cooking9)
    (:domain cooking)
    (:objects
        cucumber1 cucumber2 carrot - veggie
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
        (available cucumber1)
        (at cucumber1 cutting_board)
        (available cucumber2)
        (at cucumber2 cutting_board)
        (available carrot)
        (is-whole carrot)
        (at carrot counter)
        (is-sliced cucumber1)
        (is-sliced cucumber2)
    )
    (:goal
        (and
            (forall (?v - veggie) (in ?v bowl) )
            (forall (?v - veggie) (is-sliced ?v) )
        )
    )
)

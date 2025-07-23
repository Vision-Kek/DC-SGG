(define (problem hanoi4)
    (:domain hanoi)
    (:objects
        left_peg - peg
        middle_peg - peg
        right_peg - peg
        green_disk - disk
        orange_disk - disk
    )
    (:init
        (on-peg green_disk left_peg)
        (on-peg orange_disk middle_peg)
        (clear green_disk)
        (clear orange_disk)
        (smaller green_disk orange_disk)
    )
    (:goal
        (forall (?d - disk) (on-peg ?d right_peg))
    )
)

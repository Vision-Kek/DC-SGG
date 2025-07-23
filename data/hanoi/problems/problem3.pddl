(define (problem hanoi3)
    (:domain hanoi)
    (:objects
        left_peg - peg
        middle_peg - peg
        right_peg - peg
        orange_disk - disk
        orange_disk2 - disk
    )
    (:init
        (on orange_disk orange_disk2)
        (on-peg orange_disk2 left_peg)
        (on-peg orange_disk left_peg)
        (clear orange_disk)
        (smaller orange_disk orange_disk2)
    )
    (:goal
      (forall (?d - disk) (on-peg ?d right_peg))
    )
)
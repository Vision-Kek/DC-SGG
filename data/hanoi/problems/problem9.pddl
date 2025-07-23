(define (problem hanoi9)
    (:domain hanoi)
    (:objects
        left_peg - peg
        middle_peg - peg
        right_peg - peg
        blue_disk - disk
        pink_disk - disk
        green_disk - disk
        blue_disk2 - disk
        pink_disk2 - disk
        orange_disk - disk
    )
        (:init
            (on blue_disk pink_disk)
            (on pink_disk green_disk)
            (on green_disk blue_disk2)
            (on blue_disk2 pink_disk2)
            (on pink_disk2 orange_disk)
            (on-peg orange_disk left_peg)
            (on-peg blue_disk left_peg)
            (on-peg pink_disk left_peg)
            (on-peg green_disk left_peg)
            (on-peg blue_disk2 left_peg)
            (on-peg pink_disk2 left_peg)
            (on-peg orange_disk left_peg)
            (clear blue_disk)
            (smaller blue_disk pink_disk)
            (smaller blue_disk green_disk)
            (smaller pink_disk green_disk)
            (smaller blue_disk blue_disk2)
            (smaller pink_disk blue_disk2)
            (smaller green_disk blue_disk2)
            (smaller blue_disk pink_disk2)
            (smaller pink_disk pink_disk2)
            (smaller green_disk pink_disk2)
            (smaller blue_disk2 pink_disk2)
            (smaller blue_disk orange_disk)
            (smaller pink_disk orange_disk)
            (smaller green_disk orange_disk)
            (smaller blue_disk2 orange_disk)
            (smaller pink_disk2 orange_disk)
        )
    (:goal
      (forall (?d - disk) (on-peg ?d right_peg))
    )
)

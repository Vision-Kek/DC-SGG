(define (problem hanoi10)
    (:domain hanoi)
    (:objects
        left_peg - peg
        middle_peg - peg
        right_peg - peg
        blue_disk - disk
        pink_disk - disk
        yellow_disk - disk
        pink_disk2 - disk
        orange_disk - disk
    )
        (:init
            (on blue_disk pink_disk)
            (on pink_disk yellow_disk)
            (on yellow_disk pink_disk2)
            (on pink_disk2 orange_disk)
            (on-peg blue_disk left_peg)
            (on-peg pink_disk left_peg)
            (on-peg yellow_disk left_peg)
            (on-peg pink_disk2 left_peg)
            (on-peg orange_disk left_peg)
            (clear blue_disk)
            (smaller blue_disk pink_disk)
            (smaller blue_disk yellow_disk)
            (smaller pink_disk yellow_disk)
            (smaller blue_disk pink_disk2)
            (smaller pink_disk pink_disk2)
            (smaller yellow_disk pink_disk2)
            (smaller blue_disk orange_disk)
            (smaller pink_disk orange_disk)
            (smaller yellow_disk orange_disk)
            (smaller pink_disk2 orange_disk)
        )
    (:goal
      (forall (?d - disk) (on-peg ?d right_peg))
    )
)
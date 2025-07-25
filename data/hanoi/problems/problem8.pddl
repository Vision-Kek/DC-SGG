(define (problem hanoi8)
    (:domain hanoi)
    (:objects
        left_peg - peg
        middle_peg - peg
        right_peg - peg
        blue_disk - disk
        orange_disk2 - disk
        green_disk - disk
        pink_disk - disk
        yellow_disk - disk
        green_disk2 - disk
        orange_disk - disk
        purple_disk - disk
        blue_disk2 - disk
        pink_disk2 - disk
    )
        (:init
            (on blue_disk green_disk)
            (on green_disk pink_disk)
            (on pink_disk yellow_disk)
            (on yellow_disk green_disk2)
            (on green_disk2 orange_disk)
            (on orange_disk purple_disk)
            (on purple_disk blue_disk2)
            (on blue_disk2 pink_disk2)
            (on pink_disk2 orange_disk2)
            (on-peg blue_disk left_peg)
            (on-peg green_disk left_peg)
            (on-peg orange_disk2 left_peg)
            (on-peg pink_disk left_peg)
            (on-peg yellow_disk left_peg)
            (on-peg green_disk2 left_peg)
            (on-peg orange_disk left_peg)
            (on-peg purple_disk left_peg)
            (on-peg blue_disk2 left_peg)
            (on-peg pink_disk2 left_peg)
            (clear blue_disk)
            (smaller blue_disk orange_disk2)
            (smaller green_disk orange_disk2)
            (smaller pink_disk orange_disk2)
            (smaller yellow_disk orange_disk2)
            (smaller green_disk2 orange_disk2)
            (smaller orange_disk orange_disk2)
            (smaller purple_disk orange_disk2)
            (smaller blue_disk2 orange_disk2)
            (smaller pink_disk2 orange_disk2)
            (smaller blue_disk green_disk)
            (smaller blue_disk pink_disk)
            (smaller green_disk pink_disk)
            (smaller blue_disk yellow_disk)
            (smaller green_disk yellow_disk)
            (smaller pink_disk yellow_disk)
            (smaller blue_disk green_disk2)
            (smaller green_disk green_disk2)
            (smaller pink_disk green_disk2)
            (smaller yellow_disk green_disk2)
            (smaller blue_disk orange_disk)
            (smaller green_disk orange_disk)
            (smaller pink_disk orange_disk)
            (smaller yellow_disk orange_disk)
            (smaller green_disk2 orange_disk)
            (smaller blue_disk purple_disk)
            (smaller green_disk purple_disk)
            (smaller pink_disk purple_disk)
            (smaller yellow_disk purple_disk)
            (smaller green_disk2 purple_disk)
            (smaller orange_disk purple_disk)
            (smaller blue_disk blue_disk2)
            (smaller green_disk blue_disk2)
            (smaller pink_disk blue_disk2)
            (smaller yellow_disk blue_disk2)
            (smaller green_disk2 blue_disk2)
            (smaller orange_disk blue_disk2)
            (smaller purple_disk blue_disk2)
            (smaller blue_disk pink_disk2)
            (smaller green_disk pink_disk2)
            (smaller pink_disk pink_disk2)
            (smaller yellow_disk pink_disk2)
            (smaller green_disk2 pink_disk2)
            (smaller orange_disk pink_disk2)
            (smaller purple_disk pink_disk2)
            (smaller blue_disk2 pink_disk2)
        )
    (:goal
      (forall (?d - disk) (on-peg ?d right_peg))
    )
)
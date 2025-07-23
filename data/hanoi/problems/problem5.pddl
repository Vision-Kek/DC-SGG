(define (problem hanoi5)
    (:domain hanoi)
    (:objects
        left_peg - peg
        middle_peg - peg
        right_peg - peg
        blue_disk - disk
        pink_disk - disk
        orange_disk - disk
        purple_disk - disk
        blue_disk2 - disk
        pink_disk2 - disk
        orange_disk2 - disk
    )
(:init
    (on blue_disk pink_disk)
    (on pink_disk orange_disk)
    (on orange_disk purple_disk)
    (on purple_disk blue_disk2)
    (on blue_disk2 pink_disk2)
    (on pink_disk2 orange_disk2)
    (on-peg orange_disk2 left_peg)
    (on-peg pink_disk2 left_peg)
    (on-peg blue_disk2 left_peg)
    (on-peg purple_disk left_peg)
    (on-peg orange_disk left_peg)
    (on-peg pink_disk left_peg)
    (on-peg blue_disk left_peg)
    (clear blue_disk)
    (smaller blue_disk pink_disk)
    (smaller blue_disk orange_disk)
    (smaller pink_disk orange_disk)
    (smaller blue_disk purple_disk)
    (smaller pink_disk purple_disk)
    (smaller orange_disk purple_disk)
    (smaller blue_disk blue_disk2)
    (smaller pink_disk blue_disk2)
    (smaller orange_disk blue_disk2)
    (smaller purple_disk blue_disk2)
    (smaller blue_disk pink_disk2)
    (smaller pink_disk pink_disk2)
    (smaller orange_disk pink_disk2)
    (smaller purple_disk pink_disk2)
    (smaller blue_disk2 pink_disk2)
    (smaller blue_disk orange_disk2)
    (smaller pink_disk orange_disk2)
    (smaller orange_disk orange_disk2)
    (smaller purple_disk orange_disk2)
    (smaller blue_disk2 orange_disk2)
    (smaller pink_disk2 orange_disk2)
    )
    (:goal
      (forall (?d - disk) (on-peg ?d right_peg))
    )
)
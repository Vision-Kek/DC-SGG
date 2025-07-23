(define (problem hanoi1)
(:domain hanoi)
    (:objects
        left_peg - peg
        middle_peg - peg
        right_peg - peg
        green_disk - disk
        blue_disk - disk
        pink_disk - disk
    )
   (:init
        (on green_disk blue_disk)
        (on blue_disk pink_disk)
        (on-peg green_disk left_peg)
        (on-peg blue_disk left_peg)
        (on-peg pink_disk left_peg)
        (clear green_disk)
        (smaller green_disk blue_disk)
        (smaller green_disk pink_disk)
        (smaller blue_disk pink_disk)
    )
    (:goal
      (forall (?d - disk) (on-peg ?d right_peg) )
    )
)
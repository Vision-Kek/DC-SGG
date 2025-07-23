(define (problem hanoi1)
(:domain hanoi)
    (:objects
        left_peg - peg
        middle_peg - peg
        right_peg - peg
        purple_disk - disk
        blue_disk - disk
        pink_disk - disk
        orange_disk - disk
    )
     (:init
        (on purple_disk blue_disk)
        (on blue_disk pink_disk)
        (on pink_disk orange_disk)
        (on-peg orange_disk left_peg)
        (on-peg pink_disk left_peg)
        (on-peg blue_disk left_peg)
        (on-peg purple_disk left_peg)
        (clear purple_disk)
        (smaller purple_disk blue_disk)
        (smaller purple_disk pink_disk)
        (smaller purple_disk orange_disk)
        (smaller blue_disk pink_disk)
          (smaller blue_disk orange_disk)
        (smaller pink_disk orange_disk)
    )
    (:goal
      (forall (?d - disk) (on-peg ?d right_peg))
    )
)
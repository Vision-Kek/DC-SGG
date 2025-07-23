(define (problem hanoi3)
(:domain hanoi)
(:objects
    colored_disk - disk
    colored_disk1 - disk
    wooden_stick - peg
    wooden_stick1 - peg
    right_peg - peg
)
(:init
    ( clear colored_disk1 )
    ( on colored_disk1 colored_disk )
    ( on-peg colored_disk wooden_stick1 )
    ( on-peg colored_disk1 wooden_stick1 )
    ( smaller colored_disk1 colored_disk )
)

    (:goal
      (forall (?d - disk) (on-peg ?d right_peg))
    )
)

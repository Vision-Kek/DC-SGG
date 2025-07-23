(define (problem hanoi4)
(:domain hanoi)
(:objects
    colored_disk - disk
    colored_disk1 - disk
    right_peg - peg
    wooden_stick1 - peg
    wooden_stick2 - peg
)
(:init
    ( clear colored_disk )
    ( clear colored_disk1 )
    ( on-peg colored_disk wooden_stick1 )
    ( on-peg colored_disk1 wooden_stick1 )
    ( on-peg colored_disk1 wooden_stick2 )
    ( smaller colored_disk colored_disk1 )
)

(:goal
  (forall (?d - disk) (on-peg ?d right_peg))
)
)

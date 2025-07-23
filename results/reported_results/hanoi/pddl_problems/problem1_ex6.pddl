(define (problem hanoi1)
(:domain hanoi)
(:objects
    colored_disk - disk
    colored_disk1 - disk
    colored_disk2 - disk
    rightmost_peg - peg
    wooden_stick1 - peg
    wooden_stick2 - peg
)
(:init
    ( clear colored_disk2 )
    ( on colored_disk colored_disk1 )
    ( on colored_disk2 colored_disk )
    ( on-peg colored_disk wooden_stick2 )
    ( on-peg colored_disk1 wooden_stick2 )
    ( on-peg colored_disk2 wooden_stick2 )
    ( smaller colored_disk colored_disk1 )
    ( smaller colored_disk2 colored_disk )
    ( smaller colored_disk2 colored_disk1 )
)

    (:goal
      (forall (?d - disk) (on-peg ?d rightmost_peg))
    )
)

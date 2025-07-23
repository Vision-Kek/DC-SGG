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
    ( clear colored_disk )
    ( clear colored_disk1 )
    ( clear colored_disk2 )
    ( on-peg colored_disk wooden_stick2 )
    ( on-peg colored_disk1 wooden_stick2 )
    ( on-peg colored_disk2 wooden_stick2 )
    ( smaller colored_disk1 colored_disk )
    ( smaller colored_disk1 colored_disk2 )
    ( smaller colored_disk2 colored_disk )
)

    (:goal
        (forall (?d - disk) (on-peg ?d rightmost_peg))
    )
)

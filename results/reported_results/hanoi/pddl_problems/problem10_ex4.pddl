(define (problem hanoi10)
(:domain hanoi)
(:objects
    colored_disk - disk
    colored_disk1 - disk
    colored_disk2 - disk
    colored_disk3 - disk
    colored_disk4 - disk
    rightmost_peg - peg
    wooden_stick1 - peg
    wooden_stick2 - peg
)
(:init
    ( clear colored_disk )
    ( clear colored_disk1 )
    ( clear colored_disk2 )
    ( clear colored_disk3 )
    ( clear colored_disk4 )
    ( on-peg colored_disk1 wooden_stick2 )
    ( on-peg colored_disk2 wooden_stick2 )
    ( on-peg colored_disk4 wooden_stick2 )
    ( smaller colored_disk1 colored_disk )
    ( smaller colored_disk1 colored_disk3 )
    ( smaller colored_disk2 colored_disk )
    ( smaller colored_disk2 colored_disk1 )
    ( smaller colored_disk2 colored_disk3 )
    ( smaller colored_disk2 colored_disk4 )
    ( smaller colored_disk3 colored_disk )
    ( smaller colored_disk4 colored_disk )
    ( smaller colored_disk4 colored_disk1 )
    ( smaller colored_disk4 colored_disk3 )
)

    (:goal
        (forall (?d - disk) (on-peg ?d rightmost_peg))
    )
)

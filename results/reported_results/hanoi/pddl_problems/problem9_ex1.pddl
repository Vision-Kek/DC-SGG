(define (problem hanoi9)
(:domain hanoi)
(:objects
    colored_disk - disk
    colored_disk1 - disk
    colored_disk2 - disk
    colored_disk3 - disk
    colored_disk4 - disk
    colored_disk5 - disk
    right_peg - peg
    wooden_stick1 - peg
    wooden_stick2 - peg
)
(:init
    ( clear colored_disk5 )
    ( on colored_disk colored_disk4 )
    ( on colored_disk1 colored_disk )
    ( on colored_disk2 colored_disk1 )
    ( on colored_disk3 colored_disk2 )
    ( on colored_disk5 colored_disk3 )
    ( on-peg colored_disk wooden_stick2 )
    ( on-peg colored_disk1 wooden_stick2 )
    ( on-peg colored_disk2 wooden_stick2 )
    ( on-peg colored_disk3 wooden_stick2 )
    ( on-peg colored_disk4 wooden_stick2 )
    ( on-peg colored_disk5 wooden_stick2 )
    ( smaller colored_disk colored_disk4 )
    ( smaller colored_disk1 colored_disk )
    ( smaller colored_disk1 colored_disk4 )
    ( smaller colored_disk2 colored_disk )
    ( smaller colored_disk2 colored_disk1 )
    ( smaller colored_disk2 colored_disk4 )
    ( smaller colored_disk3 colored_disk )
    ( smaller colored_disk3 colored_disk1 )
    ( smaller colored_disk3 colored_disk2 )
    ( smaller colored_disk3 colored_disk4 )
    ( smaller colored_disk5 colored_disk )
    ( smaller colored_disk5 colored_disk1 )
    ( smaller colored_disk5 colored_disk2 )
    ( smaller colored_disk5 colored_disk3 )
    ( smaller colored_disk5 colored_disk4 )
)

    (:goal
      (forall (?d - disk) (on-peg ?d right_peg) )
    )
)

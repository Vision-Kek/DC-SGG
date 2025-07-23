(define (problem hanoi8)
(:domain hanoi)
(:objects
    colored_disk - disk
    colored_disk1 - disk
    colored_disk2 - disk
    colored_disk3 - disk
    colored_disk4 - disk
    colored_disk5 - disk
    colored_disk6 - disk
    colored_disk7 - disk
    colored_disk8 - disk
    colored_disk9 - disk
    rightmost_peg - peg
    wooden_stick1 - peg
)
(:init
    ( clear colored_disk9 )
    ( on colored_disk colored_disk2 )
    ( on colored_disk1 colored_disk3 )
    ( on colored_disk2 colored_disk6 )
    ( on colored_disk3 colored_disk4 )
    ( on colored_disk4 colored_disk )
    ( on colored_disk5 colored_disk8 )
    ( on colored_disk7 colored_disk5 )
    ( on colored_disk8 colored_disk1 )
    ( on colored_disk9 colored_disk7 )
    ( smaller colored_disk colored_disk2 )
    ( smaller colored_disk colored_disk6 )
    ( smaller colored_disk1 colored_disk )
    ( smaller colored_disk1 colored_disk2 )
    ( smaller colored_disk1 colored_disk3 )
    ( smaller colored_disk1 colored_disk4 )
    ( smaller colored_disk1 colored_disk6 )
    ( smaller colored_disk2 colored_disk6 )
    ( smaller colored_disk3 colored_disk )
    ( smaller colored_disk3 colored_disk2 )
    ( smaller colored_disk3 colored_disk4 )
    ( smaller colored_disk3 colored_disk6 )
    ( smaller colored_disk4 colored_disk )
    ( smaller colored_disk4 colored_disk2 )
    ( smaller colored_disk4 colored_disk6 )
    ( smaller colored_disk5 colored_disk )
    ( smaller colored_disk5 colored_disk1 )
    ( smaller colored_disk5 colored_disk2 )
    ( smaller colored_disk5 colored_disk3 )
    ( smaller colored_disk5 colored_disk4 )
    ( smaller colored_disk5 colored_disk6 )
    ( smaller colored_disk5 colored_disk8 )
    ( smaller colored_disk7 colored_disk )
    ( smaller colored_disk7 colored_disk1 )
    ( smaller colored_disk7 colored_disk2 )
    ( smaller colored_disk7 colored_disk3 )
    ( smaller colored_disk7 colored_disk4 )
    ( smaller colored_disk7 colored_disk5 )
    ( smaller colored_disk7 colored_disk6 )
    ( smaller colored_disk7 colored_disk8 )
    ( smaller colored_disk8 colored_disk )
    ( smaller colored_disk8 colored_disk1 )
    ( smaller colored_disk8 colored_disk2 )
    ( smaller colored_disk8 colored_disk3 )
    ( smaller colored_disk8 colored_disk4 )
    ( smaller colored_disk8 colored_disk6 )
    ( smaller colored_disk9 colored_disk )
    ( smaller colored_disk9 colored_disk1 )
    ( smaller colored_disk9 colored_disk2 )
    ( smaller colored_disk9 colored_disk3 )
    ( smaller colored_disk9 colored_disk4 )
    ( smaller colored_disk9 colored_disk5 )
    ( smaller colored_disk9 colored_disk6 )
    ( smaller colored_disk9 colored_disk7 )
    ( smaller colored_disk9 colored_disk8 )
)

    (:goal
      (forall (?d - disk) (on-peg ?d rightmost_peg))
    )
)

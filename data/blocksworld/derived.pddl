(define (domain blocksworld)

    (:derived (ontable ?x - block) 
        (not (exists (?x2- block) (on ?x ?x2)))
    )

    (:derived (clear ?x - block) 
         (not (exists (?x2- block) (on ?x2 ?x)))
    )

)

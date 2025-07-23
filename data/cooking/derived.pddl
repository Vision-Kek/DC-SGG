
(define (domain cooking)

    (:derived (is-whole ?veg - vegetable) 
        (not (is-sliced ?veg))
    )
    
    (:derived (available ?obj - object) 
        (not (exists (?gripper - gripper) (carry ?gripper ?obj)))
    )
    
    (:derived (free ?gripper - gripper) 
        (not (exists (?obj - object) (carry ?gripper ?obj)))
    )


    ;(:derived (in ?obj - object ?con - container)
    ;    (at ?obj ?con) ; if at is true for a container, it implies in.
    ;)

)

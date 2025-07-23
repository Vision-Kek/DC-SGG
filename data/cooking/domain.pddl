(define (domain cooking)

    (:types ;
        movable location - object ; a manipulatable(movable) object
        workspace - location ; can be used for cutting
        container - movable ; something can be in a container
        veggie tool - movable ; objects that can be manipulated (pick/place/...)
        cuttool - tool ; tools that can cut
        gripper ; robotic gripper can hold objects
    )

    (:predicates ;
        ; General object predicates
        (is-sliced ?veg - veggie) ; True if veggie is sliced - observed predicate
        (available ?obj - movable) ; True is object is pickable - derived predicate
        (is-whole ?veg - veggie) ; True if veggie is intact - derived predicate

        ; Robot predicates
        (carry ?gripper - gripper ?obj - movable) ; - observed predicate
        (free ?gripper - gripper) ;  - derived predicate

        ; Location predicates
        (at ?obj - movable ?loc - location) ; True if ?obj is at ?loc - observed predicate
        (in ?obj - movable ?con - container) ; True if ?obj is in ?con - observed predicate
    )

    (:action pick
        :parameters (?bot - gripper ?obj - movable ?pick_loc - location)
        :precondition(
            and
            (available ?obj)
            (free ?bot)
            (at ?obj ?pick_loc)
        )
        :effect(
            and
            (not (available ?obj))
            (carry ?bot ?obj)
            (not (free ?bot))
            (not (at ?obj ?pick_loc))
        )
    )

    (:action place
        :parameters (?bot - gripper ?obj - movable ?place_loc - location)
        :precondition(
            and
            (carry ?bot ?obj)
            (not (free ?bot))
            (not (at ?obj ?place_loc))
        )
        :effect(
            and
            (available ?obj)
            (free ?bot)
            (at ?obj ?place_loc)
            (not (carry ?bot ?obj))
        )
    )

     (:action place_in
        :parameters (?bot - gripper ?obj - movable ?place_loc - container)
        :precondition(
            and
            (carry ?bot ?obj)
            (not (free ?bot))
            (not (in ?obj ?place_loc))
        )
        :effect(
            and
            (available ?obj)
            (free ?bot)
            (in ?obj ?place_loc)
            (not (carry ?bot ?obj))
        )
    )

    (:action slice
        :parameters (?bot - gripper ?veg - veggie ?cuttool - cuttool ?loc - workspace)
        :precondition(
            and
            (carry ?bot ?cuttool)
            (is-whole ?veg)
            (not (is-sliced ?veg))
            (at ?veg ?loc)
        )
        :effect(
            and
            (is-sliced ?veg)
            (not (is-whole ?veg))
        )
    )
  )

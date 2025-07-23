```pddl
(:goal
    (and
        (forall (?v - veggie) (in ?v bowl) )
        (forall (?v - veggie) (is-sliced ?v) )
    )
)
```
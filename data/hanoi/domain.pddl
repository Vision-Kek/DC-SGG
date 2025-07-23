(define (domain hanoi)
  (:types
    disk
    peg
  )
  (:predicates
    (on ?d_above - disk ?d_below - disk)          ; A disk is on a peg - observed predicate
    (on-peg ?d - disk ?p - peg)          ; A disk is on a peg - observed predicate
    (clear ?d - disk)                 ; A disk has no other disk on top - derived predicate
    (smaller ?d1 - disk ?d2 - disk)  ; A disk is smaller than another disk - observed predicate
  )

  ; Action: move a disk from one peg to another
  (:action move
    :parameters (?d - disk ?from - peg ?to - peg)
    :precondition (and
                    (on-peg ?d ?from)             ; The disk is on the "from" peg
                    (clear ?d)              ; The disk to move has nothing on top of it
                    (not (on-peg ?d ?to))        ; The disk should not already be on the "to" peg
                    ; Ensure no larger disk is already on the "to" peg
                    (forall (?d2 - disk)
                      (or
                        (not (on-peg ?d2 ?to))          ; There is a disk on the "to" peg
                        (smaller ?d ?d2)      ; The disk being moved must be smaller
                      )
                    )
                   )
    :effect (and
              ; The disk that was below ?d on ?from is now clear
              (forall (?d2 - disk)
                (when 
                 (on ?d ?d2)
                 (and (clear ?d2) (not(on ?d ?d2)))
                )
              )
              (not (on-peg ?d ?from))        ; The disk is no longer on the "from" peg
              (on-peg ?d ?to)               ; The disk is now on the "to" peg

              ; The disk below ?d is no longer clear
              (forall (?d2 - disk)
                (when 
                 (and (on-peg ?d2 ?to) (clear ?d2) ) ; if disk is on top of target peg
                 (and 
                    (not (clear ?d2))  ; than this disk is no longer clear 
                    (on ?d ?d2) ; and ?d is now on top of it
                 ) 
                )
              )
            )
    )
)
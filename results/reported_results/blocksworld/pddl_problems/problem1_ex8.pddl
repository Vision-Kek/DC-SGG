(define (problem blocksworld1)
(:domain blocksworld)
(:objects
    green_block - block 
    yellow_block - block 
    arm - robot 
    pink_block - block 
    red_block - block 
)

(:init
    ( clear green_block )
    ( clear pink_block )
    ( clear yellow_block )
    ( handempty arm )
    ( on pink_block red_block )
    ( ontable green_block )
    ( ontable red_block )
    ( ontable yellow_block )
)

    (:goal (and (on pink_block red_block) (on red_block yellow_block) (on yellow_block green_block)))
)

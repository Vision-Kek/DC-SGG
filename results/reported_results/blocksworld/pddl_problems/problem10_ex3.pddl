(define (problem blocksworld10)
(:domain blocksworld)
(:objects
    blue_block - block 
    arm - robot 
    yellow_block - block 
    red_block - block 
    orange_block - block 
    pink_block - block 
    green_block - block 
)

(:init
    ( clear blue_block )
    ( clear green_block )
    ( clear orange_block )
    ( clear pink_block )
    ( clear red_block )
    ( clear yellow_block )
    ( handempty arm )
    ( ontable blue_block )
    ( ontable green_block )
    ( ontable orange_block )
    ( ontable pink_block )
    ( ontable red_block )
    ( ontable yellow_block )
)

    (:goal (and (on blue_block pink_block) (on pink_block red_block) (on yellow_block orange_block) (on orange_block green_block) (clear yellow_block) (clear blue_block)))
)

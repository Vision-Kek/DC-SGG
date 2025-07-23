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
    ( clear green_block )
    ( clear pink_block )
    ( clear red_block )
    ( handempty arm )
    ( on green_block orange_block )
    ( on orange_block yellow_block )
    ( on pink_block blue_block )
    ( ontable blue_block )
    ( ontable red_block )
    ( ontable yellow_block )
)

    (:goal (and (on blue_block pink_block) (on pink_block red_block) (on yellow_block orange_block) (on orange_block green_block)))
)

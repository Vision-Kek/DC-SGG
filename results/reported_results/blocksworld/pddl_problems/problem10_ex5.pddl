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
    ( clear orange_block )
    ( handempty arm )
    ( on orange_block green_block )
    ( on orange_block yellow_block )
    ( on pink_block blue_block )
    ( on red_block pink_block )
    ( on yellow_block red_block )
    ( ontable blue_block )
    ( ontable green_block )
)

(:goal (and (on blue_block pink_block) (on pink_block red_block) (on yellow_block orange_block) (on orange_block green_block)))
)

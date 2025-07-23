(define (problem blocksworld5)
(:domain blocksworld)
(:objects
    green_block - block 
    blue_block - block 
    arm - robot 
    yellow_block - block 
    orange_block - block 
    red_block - block 
)

(:init
    ( clear green_block )
    ( handempty arm )
    ( on blue_block red_block )
    ( on green_block orange_block )
    ( on orange_block blue_block )
    ( on red_block yellow_block )
    ( ontable yellow_block )
)

    (:goal (and (on yellow_block red_block) (on red_block blue_block) (on blue_block orange_block) (on orange_block green_block)))
)

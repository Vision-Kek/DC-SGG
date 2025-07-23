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
    ( clear blue_block )
    ( clear green_block )
    ( clear orange_block )
    ( clear red_block )
    ( clear yellow_block )
    ( handempty arm )
    ( ontable blue_block )
    ( ontable green_block )
    ( ontable orange_block )
    ( ontable red_block )
    ( ontable yellow_block )
)

    (:goal (and (on yellow_block red_block) (on red_block blue_block) (on blue_block orange_block) (on orange_block green_block)))
)

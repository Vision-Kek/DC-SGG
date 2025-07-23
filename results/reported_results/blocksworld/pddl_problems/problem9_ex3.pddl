(define (problem blocksworld9)
(:domain blocksworld)
(:objects
    blue_block - block 
    arm - robot 
    yellow_block - block 
    red_block - block 
    orange_block - block 
    purple_block - block 
    green_block - block 
)

(:init
    ( clear orange_block )
    ( clear purple_block )
    ( handempty arm )
    ( on blue_block green_block )
    ( on green_block yellow_block )
    ( on purple_block blue_block )
    ( on yellow_block red_block )
    ( ontable orange_block )
    ( ontable red_block )
)

    (:goal (and (on purple_block blue_block) (on blue_block green_block) (on green_block yellow_block) (on yellow_block red_block) (on red_block orange_block) (clear orange_block) (clear purple_block)))
)

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
    ( clear blue_block )
    ( clear green_block )
    ( clear orange_block )
    ( clear purple_block )
    ( clear red_block )
    ( clear yellow_block )
    ( handempty arm )
    ( ontable blue_block )
    ( ontable green_block )
    ( ontable orange_block )
    ( ontable purple_block )
    ( ontable red_block )
    ( ontable yellow_block )
)

(:goal (and (on purple_block blue_block) (on blue_block green_block) (on green_block yellow_block) (on yellow_block red_block) (on red_block orange_block)))
)

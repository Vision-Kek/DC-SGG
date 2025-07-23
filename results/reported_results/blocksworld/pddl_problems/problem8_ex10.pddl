(define (problem blocksworld8)
(:domain blocksworld)
(:objects
    green_block - block 
    arm - robot 
    yellow_block - block 
    orange_block - block 
    purple_block - block 
    pink_block - block 
    red_block - block 
)

(:init
    ( clear green_block )
    ( clear orange_block )
    ( clear pink_block )
    ( clear purple_block )
    ( clear red_block )
    ( clear yellow_block )
    ( handempty arm )
    ( ontable green_block )
    ( ontable orange_block )
    ( ontable pink_block )
    ( ontable purple_block )
    ( ontable red_block )
    ( ontable yellow_block )
)

    (:goal (and (on green_block yellow_block) (on yellow_block pink_block) (on purple_block orange_block) (on orange_block red_block)))
)

(define (problem blocksworld3)
(:domain blocksworld)
(:objects
    green_block - block 
    arm - robot 
    yellow_block - block 
    purple_block - block 
    pink_block - block 
    red_block - block 
)

(:init
    ( clear green_block )
    ( clear pink_block )
    ( clear purple_block )
    ( clear red_block )
    ( clear yellow_block )
    ( handempty arm )
    ( ontable green_block )
    ( ontable pink_block )
    ( ontable purple_block )
    ( ontable red_block )
    ( ontable yellow_block )
)

(:goal (and (on yellow_block green_block) (on green_block pink_block) (on red_block purple_block)))
)

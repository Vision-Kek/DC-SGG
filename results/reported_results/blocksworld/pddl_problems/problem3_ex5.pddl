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
    ( clear pink_block )
    ( clear purple_block )
    ( clear yellow_block )
    ( handempty arm )
    ( on purple_block red_block )
    ( on yellow_block green_block )
    ( ontable green_block )
    ( ontable pink_block )
    ( ontable red_block )
)

(:goal (and (on yellow_block green_block) (on green_block pink_block) (on red_block purple_block)))
)

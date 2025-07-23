(define (problem blocksworld7)
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
    ( clear orange_block )
    ( clear red_block )
    ( clear yellow_block )
    ( handempty arm )
    ( on pink_block green_block )
    ( on red_block purple_block )
    ( on yellow_block pink_block )
    ( ontable green_block )
    ( ontable orange_block )
    ( ontable purple_block )
)

    (:goal (and (on yellow_block pink_block) (on pink_block green_block) (on green_block red_block) (on red_block purple_block) (on purple_block orange_block) (clear yellow_block)))
)

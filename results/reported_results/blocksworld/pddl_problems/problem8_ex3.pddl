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
    ( clear red_block )
    ( handempty arm )
    ( on orange_block purple_block )
    ( on pink_block yellow_block )
    ( on purple_block pink_block )
    ( on red_block orange_block )
    ( on yellow_block green_block )
    ( ontable green_block )
)

    (:goal (and (on green_block yellow_block) (on yellow_block pink_block) (on purple_block orange_block) (on orange_block red_block) (clear purple_block) (clear green_block)))
)

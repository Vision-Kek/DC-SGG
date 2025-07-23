(define (problem blocksworld6)
(:domain blocksworld)
(:objects
    colored_block2 - block 
    arm - robot 
    yellow_block - block 
    orange_block - block 
    purple_block - block 
    pink_block - block 
)

(:init
    ( clear orange_block )
    ( clear purple_block )
    ( handempty arm )
    ( on orange_block colored_block2 )
    ( on pink_block yellow_block )
    ( on purple_block pink_block )
    ( ontable colored_block2 )
    ( ontable yellow_block )
)

    (:goal (and (on pink_block purple_block) (on yellow_block orange_block) (clear yellow_block) (clear pink_block)))
)

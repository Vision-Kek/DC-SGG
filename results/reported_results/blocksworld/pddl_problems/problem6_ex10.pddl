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
    ( clear colored_block2 )
    ( clear orange_block )
    ( clear pink_block )
    ( clear purple_block )
    ( clear yellow_block )
    ( handempty arm )
    ( ontable colored_block2 )
    ( ontable orange_block )
    ( ontable pink_block )
    ( ontable purple_block )
    ( ontable yellow_block )
)

(:goal (and (on pink_block purple_block) (on yellow_block orange_block)))
)

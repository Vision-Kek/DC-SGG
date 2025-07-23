(define (problem blocksworld4)
(:domain blocksworld)
(:objects
    blue_block - block 
    arm - robot 
    yellow_block - block 
    orange_block - block 
    purple_block - block 
    red_block - block 
)

(:init
    ( clear blue_block )
    ( clear orange_block )
    ( clear purple_block )
    ( clear yellow_block )
    ( handempty arm )
    ( on purple_block red_block )
    ( ontable blue_block )
    ( ontable orange_block )
    ( ontable red_block )
    ( ontable yellow_block )
)

    (:goal (and (on orange_block yellow_block) (on yellow_block blue_block) (on blue_block purple_block) (on purple_block red_block)))
)

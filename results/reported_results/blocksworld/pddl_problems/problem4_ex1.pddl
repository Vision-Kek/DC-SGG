(define (problem blocksworld4)
(:domain blocksworld)
(:objects
    colored_block3 - block 
    arm - robot 
    yellow_block - block 
    orange_block - block 
    blue_purple_block - block 
    red_block - block 
)

(:init
    ( clear blue_purple_block )
    ( clear colored_block3 )
    ( clear orange_block )
    ( clear red_block )
    ( clear yellow_block )
    ( handempty arm )
    ( ontable blue_purple_block )
    ( ontable colored_block3 )
    ( ontable orange_block )
    ( ontable red_block )
    ( ontable yellow_block )
)

    (:goal (and (on orange_block yellow_block) (on yellow_block blue_purple_block) (on blue_purple_block red_block)))
)

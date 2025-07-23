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
    ( clear yellow_block )
    ( handempty arm )
    ( on colored_block3 red_block )
    ( on yellow_block red_block )
    ( ontable blue_purple_block )
    ( ontable orange_block )
    ( ontable red_block )
)

    (:goal (and (on orange_block yellow_block) (on yellow_block blue_purple_block) (on blue_purple_block red_block)))
)

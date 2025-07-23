(define (problem blocksworld2)
(:domain blocksworld)
(:objects
    blue_block - block 
    arm - robot 
    purple_block - block 
    pink_block - block 
    red_block - block 
)

(:init
    ( clear pink_block )
    ( clear red_block )
    ( handempty arm )
    ( on pink_block purple_block )
    ( on purple_block blue_block )
    ( ontable blue_block )
    ( ontable red_block )
)

    (:goal (and (on red_block blue_block) (on blue_block purple_block) (on purple_block pink_block)))
)

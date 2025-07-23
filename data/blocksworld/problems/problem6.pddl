(define (problem blocksworld6)
    (:domain blocksworld)
    (:objects
        purple_block - block
        pink_block - block
        yellow_block - block
        orange_block - block
        red_block - block
        bot - robot
    )
    (:init
        (ontable yellow_block)
        (ontable red_block)
        (clear purple_block)
        (clear orange_block)
        (on purple_block pink_block)
        (on pink_block yellow_block)
        (on orange_block red_block)
        (handempty bot)
    )
    (:goal (and (on pink_block purple_block) (on yellow_block orange_block)))
)
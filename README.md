# Mendelbrot set implementation #

Instructions found here: https://www.quora.com/What-are-the-most-satisfying-programming-hobby-projects-that-can-be-done-is-a-few-hours

Not so much as a glance at any solution specific code, except a little help from this reddit post: https://www.reddit.com/r/Python/comments/9flpm6/if_anyone_wants_to_check_out_my_3_hour_2_hours/

Inputs for photoset: 
    center x: 0.3876
    center y: -0.03745
    initial resolution: 0.000001 # 'step', 'pixel', or 'unit'
    size of image: 10000 # (10000 x 10000)px
    max number of iterations: 200
    frames: 1
    next frame scale: doesn't matter

Inputs for gif: 
    center x: 0.3876
    center y: -0.03745
    initial resolution: 0.00001
    size of image: 750
    max number of iterations: 100
    number of frames: 25
    next frame scale: 0.6

TODO: Improve method of determining how quickly the point diverges/improve coloring system
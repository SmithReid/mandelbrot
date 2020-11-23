# Code Written by Reid Smith
# Began on 9/13/2018
# Creative Commons license
# A basic implementation of the Mandelbrot set

# The script collects some inputs, and then saves a .gif and each frame to disk

# Wow, I've picked up some better practices since I wrote this...

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import multiprocessing

class Complex(object):
    """
    A basic implementation of complex numbers.  
    Functionality is limited to that  which is required by the mandelbrot problem.
    """
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
    def square(self):
        return Complex(self.real ** 2 - self.imaginary ** 2, 2 * self.real * self.imaginary)
    def add(self, other):
        return Complex(self.real + other.real, self.imaginary + other.imaginary)
    def __eq__(self, other):
        if self.real == other.real and self.imaginary == other.imaginary:
            return True
        else: 
            return False
    def approx_eq(self, other):
        if int(self.real * 100) == int(other.real * 100)\
            and int(self.imaginary * 100) == int(other.imaginary * 100):
            print("We did it!")
            return True
        else: 
            return False
    def __repr__(self):
        return '{} + {}i'.format(str(self.real), str(self.imaginary))

def frange(x, y, jump):
    """
    Straight off of stackoverflow
    Inputs: 
        x: the beginning of the range
        y: the end of the range
        jump: the step
    Outputs: 
        The function is basically range() for floats; a generator for generating floats in [x, y) with step 'jump'
    """
    while x < y:
        yield x
        x += jump

def mendelbrot(x, y, max_iter):
    """
    Inputs:
        x: the real value in the complex plane
        y: the imaginary value in the complex plane
        max_iter: the maximum number of iterations before we will consider the point to converge
    Outputs: 
        an integer color
    Function: 
        For a complex number, c = x + yi, decide whether the series: z[n] = z[n-1]^2 + c converges, and if it diverges, how quickly it does so. 
    TODO: come up with a better way of measuring how quickly the series diverges, if it diverges
    """
    z = Complex(0, 0)
    for i in range(max_iter):
        try: 
            z = z.square().add(Complex(x, y))
            if z.real > 2: 
                return i
        except: 
            return i

    return max_iter

def sort_intermediates(arr):
    """
    Sorts an array where each element is in the string form "{}.png".format(frame_number)
    Inputs: 
        arr: the array
    Outputs: 
        The properly sorted array
    """
    arr = [int(x.strip('.png')) for x in arr]
    return [str(x) + '.png' for x in sorted(arr)]

def render_frame(x_center, y_center, initial_resolution, n_pixels, max_iter, frame_number, size_per_frame):
    """
    Renders and saves a single frame of the .gif
    Inputs: 
        x_center: the x center of the frame
        y_center: the y center of the frame
        initial_resolution: the resolution of frame 1
        n_pixels: the frame is a square. This is the number of pixels on either side
        max_iter: the maximum number of iterations of the mandelbrot calculation
        frame_number: the frame number
        size_per_frame: see the first line of this function. Each frame is scaled by this value
    Outputs: 
        saves the frame to disk
    """
    # change values specific to the frame
    iter_step = 125
    resolution = initial_resolution * (size_per_frame ** (frame_number - 1))
    max_iter = max_iter + (iter_step * frame_number)

    # calculate the limits of the image
    x_min = x_center - ((n_pixels / 2) * resolution)
    x_max = x_center + ((n_pixels / 2) * resolution)
    y_min = y_center - ((n_pixels / 2) * resolution)
    y_max = y_center + ((n_pixels / 2) * resolution)

    # run the mandelbrot calculation for each pixel
    img = np.zeros((n_pixels, n_pixels))
    for i, x in zip(range(n_pixels), frange(x_min, x_max, resolution)):
        for j, y in zip(range(n_pixels - 1, -1, -1), frange(y_min, y_max, resolution)):
            img[j][i] = mendelbrot(x, y, max_iter)
    np.savetxt('arrays/{}_array.csv'.format(str(frame_number)), img)

    # save the image
    plt.figure(figsize=(18, 18))
    plt.axis('on')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.imshow(img, interpolation='none', extent=[x_min, x_max, y_min, y_max])
    plt.savefig('intermediates/{}.png'.format(str(frame_number)).zfill(4))
    plt.close()
    print("Frame {} rendered.".format(str(frame_number)))

if __name__ == "__main__":
    # remove the old intermediate images
    old_images = os.listdir("intermediates")
    for filename in old_images:
        os.remove('intermediates/{}'.format(filename))

    x_center = -0.74951145384
    y_center = 0.04961979335
    resolution = 0.0000001
    n_pixels = 256
    max_iter = 2500
    frames = 12
    size_per_frame = 0.25
    
    start_time = datetime.now()

    # for each frame, create and start a process
    multiprocessing.set_start_method('spawn')
    processes = []
    for frame_number in range(1, frames + 1):
        processes.append(multiprocessing.Process(
            target=render_frame, 
            args=(
                x_center, 
                y_center, 
                resolution, 
                n_pixels, 
                max_iter, 
                frame_number, 
                size_per_frame)))
    if len(processes) > 24: 
        while len(processes) > 0:
            active_processes = []
            for i in range(multiprocessing.cpu_count()):
                active_processes.append(processes.pop(0))
            for process in active_processes:
                process.start()
            for process in active_processes:
                process.join()
            del active_processes
    else: 
        for process in processes: 
            process.start()
        for process in processes: 
            process.join()

    # compile the gif from the images and save
    intermediates = sort_intermediates(os.listdir('intermediates'))
    images = []
    for filename in intermediates:
        images.append(imageio.imread('intermediates/{}'.format(filename)))
    print("Rendering gif.")
    imageio.mimsave('final/{}.gif'.format(str(datetime.now().strftime('%Y-%m-%d--%H-%M'))), images)
    print("Runtime: {}".format(datetime.now() - start_time))


"""
Next Run: 
<<<<<<< HEAD
0.35204, -0.098
=======
-0.735, 0.208
>>>>>>> e54532fa17905ba29a6a955dc3a80d93e461837a
"""




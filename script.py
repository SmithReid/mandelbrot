# Code Written by Reid Smith
# Began on 9/13/2018
# Creative Commons license
# A basic implementation of the Mandelbrot set

# The script collects some inputs, and then saves a .gif and each frame to disk

from datetime import datetime
start_time = datetime.now()
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import multiprocessing

class Complex(object):
    """
    A basic implementation of complex numbers.  
    Functionality is limited to that  which is required by my problem.
    """
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
    def square(self):
        return Complex(self.real ** 2 - self.imaginary ** 2, 2 * self.real * self.imaginary)
    def add(self, number):
        return Complex(self.real + number.real, self.imaginary + number.imaginary)
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
    z = [Complex(0, 0)]
    for i in range(max_iter):
        try: 
            z.append(z[-1].square().add(Complex(x, y)))
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
    resolution = initial_resolution * (size_per_frame ** (frame_number - 1))
    x_min = x_center - ((n_pixels / 2) * resolution)
    x_max = x_center + ((n_pixels / 2) * resolution)
    y_min = y_center - ((n_pixels / 2) * resolution)
    y_max = y_center + ((n_pixels / 2) * resolution)

    img = np.zeros((n_pixels, n_pixels))
    for i, x in zip(range(n_pixels), frange(x_min, x_max, resolution)):
        for j, y in zip(range(n_pixels), frange(x_min, x_max, resolution)):
            img[j][i] = mendelbrot(x, y, max_iter)

    plt.figure(figsize=(12, 8))
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.imshow(img, interpolation='none', extent=[x_min, x_max, y_min, y_max])
    plt.savefig('intermediates/{}.png'.format(str(frame_number)).zfill(4))
    plt.close()
    print("Frame #{} complete".format(str(frame_number)))

if __name__ == "__main__":
    old_images = os.listdir("intermediates")
    for filename in old_images:
        os.remove('intermediates/{}'.format(filename))

    x_center = float(input("Please enter center x.\n"))
    y_center = float(input("Please enter center y.\n"))
    resolution = float(input("Please enter starting resolution.\n"))
    n_pixels = int(input("Please enter the size of the squre (pixels).\n"))
    max_iter = int(input("Please enter the maximum number of iterations.\n"))
    frames = int(input("Please enter the number of frames.\n"))
    size_per_frame = float(input("Next frame scale?\n"))

    multiprocessing.set_start_method('spawn')
    processes = []
    for frame_number in range(1, frames + 1):
        processes.append(multiprocessing.Process(target=render_frame, args=(x_center, y_center, resolution, n_pixels, max_iter, frame_number, size_per_frame)))
    active_processes = []
    for process in processes:
        active_processes.append(process)
        if len(active_processes) == multiprocessing.cpu_count():
            for active_process in active_processes:
                active_process.start()
            for active_process in active_processes:
                active_process.join()
            active_processes = []
    if len(active_processes) > 0:
        for active_process in active_processes:
            active_process.start()
        for active_process in active_processes:
            active_process.join()

    intermediates = sort_intermediates(os.listdir('intermediates'))
    images = []
    for filename in intermediates:
        images.append(imageio.imread('intermediates/{}'.format(filename)))
    imageio.mimsave('final/{}.gif'.format(str(datetime.now().strftime('%Y-%m-%d_%H:%M'))), images)
    print("Runtime = {}".format(datetime.now() - start_time))







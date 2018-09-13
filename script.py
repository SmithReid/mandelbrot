import numpy as np
import matplotlib.pyplot as plt

class Complex(object):
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
    while x < y:
        yield x
        x += jump

def mendelbrot(x, y):
    arr = [Complex(0, 0)]
    n_iters = 0
    try_again = True
    while try_again == True and n_iters < 200:
        try:
            arr.append(arr[-1].square().add(Complex(x, y)))
        except: 
            try_again = False
        n_iters += 1
    return len(arr)

if __name__ == "__main__":
    x_center = float(input("Please enter center x.\n"))
    y_center = float(input("Please enter center y.\n"))
    resolution = float(input("Please enter resolution.\n"))
    n_pixels = int(input("Please enter the size of the image.\n"))

    x_min = x_center - ((n_pixels / 2) * resolution)
    x_max = x_center + ((n_pixels / 2) * resolution)
    y_min = y_center - ((n_pixels / 2) * resolution)
    y_max = y_center + ((n_pixels / 2) * resolution)

    img = np.zeros((n_pixels, n_pixels))
    for i, x in zip(range(n_pixels), frange(x_min, x_max, resolution)):
        for j, y in zip(range(n_pixels), frange(x_min, x_max, resolution)):
            img[j][i] = mendelbrot(x, y)
        print(i)

    plt.figure(figsize=(10, 10))
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.imshow(img, interpolation='none', extent=[x_min, x_max, y_min, y_max])
    plt.show()
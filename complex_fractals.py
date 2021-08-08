from PIL import Image
from numba import njit
from numba import cuda
import numpy as np
import sys, inspect
import math

#TODO GPU render option: http://numba.pydata.org/numba-doc/latest/cuda/
#  2 run functions in each subclass (one for gpu, one for cpu)
#  based off of passed boolean value gpu (True or False for gpu or cpu respectively)

#TODO: add additional classes for zoom of each fractal

class Fractal():
    def __init__(self, min_x, max_x, min_y, max_y, filename, color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, escape_radius=4):

        self.dimen_x, self.dimen_y = self.__set_dimensions(xdim, aspect_ratio)
        self.iterations = max_iterations
        self.R = escape_radius

        self.X = self.__setX(min_x, max_x, self.dimen_x)
        self.Y = self.__setY(min_y, max_y, self.dimen_y)

        self.img_data = np.zeros((self.dimen_y, self.dimen_x), dtype=np.float32)
        self.is_not_diverged = np.ones((self.dimen_y, self.dimen_x), dtype=np.float32)

        self.filename = filename
        self.__set_color_maps()
        self.cm = self.color_maps["pink-teal"] if color_map is None else self.color_maps[color_map]

    def __set_dimensions(self, xdim, aspect_ratio):
        if aspect_ratio == "16:9":
            ydim = math.floor((xdim/16.0)*9)
        elif aspect_ratio == "21:9":
            ydim = math.floor((xdim/21.0)*9)
        else:
            ydim = xdim
        return xdim, ydim

    def __setX(self, a, b, dimen):
        return np.linspace(a, b, dimen).reshape((1, dimen))
    
    def __setY(self, a, b, dimen):
        return np.linspace(a, b, dimen).reshape((dimen, 1))
    
    def color(self, z, i, R):
        if abs(z) < R:
            return self.cm[0], self.cm[1], self.cm[2]
        v = np.log2(i + R - np.log2(np.log2(abs(z)))) / 5
        if v < 1.0:
            v = max(0,v)
            return v**self.cm[3], v**self.cm[4], v**self.cm[5] # outer
        else:
            v = max(0, 2 - v)
            return v**self.cm[6], v**self.cm[7], v**self.cm[8] # inner

    def _get_colors(self):
        #print("  -assigning colors")
        r, g, b = np.frompyfunc(self.color, 3, 3)(self.z, self.img_data, self.R)
        img_c = np.dstack((r,g,b))
        return np.uint8(img_c * 255)

    def _update_img_data(self):
        self.is_not_diverged = (np.abs(self.z)<self.R).astype(np.float32) #0->diverged, 1->not
        self.img_data += self.is_not_diverged

    def _create_image(self, color_array, filename):
        #print("  -creating images")
        display = Image.fromarray(color_array, 'RGB')
        display.save(filename)

    def __set_color_maps(self):
        self.color_maps = {
            "blue-sepia":   [0.00, 0.00, 0.00, 4.00, 2.50, 1.00, 1.00, 1.50, 3.00],
            "green-purple": [0.00, 0.00, 0.00, 2.50, 1.00, 4.00, 1.50, 3.00, 1.00],
            "pink-teal":    [0.00, 0.00, 0.00, 1.00, 4.00, 2.50, 3.00, 1.00, 1.50],
            "orange-blue":  [0.00, 0.00, 0.00, 1.00, 2.50, 4.00, 3.00, 1.50, 1.00],
            "indigo-green": [0.00, 0.00, 0.00, 2.50, 4.00, 1.00, 1.50, 1.00, 3.00],

            "black-white":  [0.00, 0.00, 0.00, 10.0, 10.0, 10.0, 1.00, 1.00, 1.00],
            "white-black":  [0.00, 0.00, 0.00, 1.00, 1.00, 1.00, 2.00, 2.00, 2.00],
            
            "purple":       [0.50, 0.00, 1.00, 1.50, 4.00, 1.00, 1.20, 1.80, 1.00],
            "orange":       [1.00, 0.50, 0.00, 1.00, 1.50, 4.00, 1.00, 1.20, 1.80],
            "cyan":         [0.00, 1.00, 0.50, 4.00, 1.00, 1.50, 1.80, 1.00, 1.20],

            "blue":         [0.00, 0.50, 1.00, 4.00, 1.50, 1.00, 1.80, 1.20, 1.00], 
            "lime":         [0.50, 1.00, 0.00, 1.50, 1.00, 4.00, 1.20, 1.00, 1.80],
            "pink":         [1.00, 0.00, 0.50, 1.00, 4.00, 1.50, 1.00, 1.80, 1.20],

            "seablue":      [0.00, 0.22, 1.00, 4.00, 2.90, 1.00, 1.80, 1.70, 1.00],
            "green":        [0.22, 1.00, 0.00, 2.90, 1.00, 4.00, 1.70, 1.00, 1.80],
            "watermelon":   [1.00, 0.00, 0.22, 1.00, 4.00, 2.90, 1.00, 1.80, 1.70],

            "red":          [1.00, 0.22, 0.00, 1.00, 2.90, 4.00, 1.00, 1.70, 1.80],
            "indigo":       [0.22, 0.00, 1.00, 2.90, 4.00, 1.00, 1.70, 1.80, 1.00],
            "shamrock":     [0.00, 1.00, 0.22, 4.00, 1.00, 2.90, 1.80, 1.00, 1.70],

            "barbour":      [0.04, 0.39, 0.08, 3.00, 1.50, 3.00, 1.40, 1.10, 1.40],
            "wine":         [0.39, 0.08, 0.04, 1.50, 3.00, 3.00, 1.10, 1.40, 1.40],
            "midnightblue": [0.08, 0.04, 0.39, 3.00, 3.00, 1.50, 1.40, 1.40, 1.10],

            "yellow":       [0.70, 0.70, 0.20, 1.00, 1.00, 3.00, 1.00, 1.00, 1.80],
            "magenta":      [0.70, 0.20, 0.70, 1.00, 3.00, 1.00, 1.00, 1.80, 1.00],
            "teal":         [0.20, 0.70, 0.70, 3.00, 1.00, 1.00, 1.80, 1.00, 1.00],
        }


class Mandelbrot(Fractal):
    def __init__(self, filename="mandelbrot.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Mandelbrot")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-3.33, 2.0, -1.5, 1.5]
            elif aspect_ratio == "21:9":
                coords = [-4.48, 2.69, -1.5, 1.5]
            else:
                coords = [-2.20, 0.80, -1.5, 1.5]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: 2ab + Im(c)
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real)+1j*(2*self.z.real*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class Mandelbar(Fractal):
    def __init__(self, filename="mandelbar.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Mandelbar")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-1.78, 1.78, -1, 1]
            elif aspect_ratio == "21:9":
                coords = [-2.38, 2.38, -1, 1]
            else:
                coords = [-1.20, 0.80, -1, 1]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: -2ab + Im(c)
            self.z = z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real)+1j*(-2*self.z.real*self.z.imag+self.c.imag) + self.c, self.z)
            self._update_img_data()
        return self._get_colors()


class PerpendicularMandelbrot(Fractal):
    def __init__(self, filename="perpendicularMandelbrot.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Perpendicular Mandelbrot")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-3.0, 2.33, -1.5, 1.5]
            elif aspect_ratio == "21:9":
                coords = [-4.03, 3.14, -1.5, 1.5]
            else:
                coords = [-1.90, 1.10, -1.5, 1.5]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: -2b|a| + Im(c)
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real)+1j*(-2*self.z.imag*abs(self.z.real)+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class Celtic(Fractal):
    def __init__(self, filename="celtic.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Celtic")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-4.12, 3.0, -2, 2]
            elif aspect_ratio == "21:9":
                coords = [-5.52, 4.03, -2, 2]
            else:
                coords = [-2.70, 1.30, -2, 2]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: 2ab + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real)+1j*(2*self.z.real*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class CelticMandelbar(Fractal):
    def __init__(self, filename="celticMandelbar.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Celtic Mandelbar")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-3.33, 2.0, -1.5, 1.5]
            elif aspect_ratio == "21:9":
                coords = [-4.48, 2.69, -1.5, 1.5]
            else:
                coords = [-2.20, 0.80, -1.5, 1.5]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: -2ab + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real)+1j*(-2*self.z.real*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class PerpendicularCeltic(Fractal):
    def __init__(self, filename="perpendicularCeltic.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Perpendicular Celtic")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-3.33, 2.0, -1.5, 1.5]
            elif aspect_ratio == "21:9":
                coords = [-4.48, 2.69, -1.5, 1.5]
            else:
                coords = [-2.20, 0.80, -1.5, 1.5]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: -2b|a| + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real)+1j*(-2*abs(self.z.real)*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class BurningShip(Fractal):
    def __init__(self, filename="burningShip.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Burning Ship")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-3.0, 2.33, -2.0, 1.0]
            elif aspect_ratio == "21:9":
                coords = [-4.03, 3.14, -2.0, 1.0]
            else:
                coords = [-1.80, 1.20, -2.0, 1.0]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: -2|ab|
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real) + 1j*(2*abs(self.z.imag*self.z.real) + self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class HeartMandelbrot(Fractal):
    def __init__(self, filename="heartMandelbrot.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Heart Mandelbrot")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-2.22, 1.33, -1, 1]
            elif aspect_ratio == "21:9":
                coords = [-2.99, 1.79, -1, 1]
            else:
                coords = [-1.55, 0.45, -1, 1]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: 2b|a| + Im(c)
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real) + 1j*(2*self.z.imag*abs(self.z.real)+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class PerpendicularBurningShip(Fractal):
    def __init__(self, filename="perpendicularBurningShip.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Perpendicular Burning Ship")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-3.0, 2.33, -1.5, 1.5]
            elif aspect_ratio == "21:9":
                coords = [-4.03, 3.14, -1.5, 1.5]
            else:
                coords = [-1.85, 1.15, -1.5, 1.5]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: -2a|b| + Im(c)
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real) + 1j*(2*self.z.real*abs(self.z.imag)+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class Buffalo(Fractal):
    def __init__(self, filename="buffalo.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Buffalo")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-3.33, 2.0, -2.0, 1.0]
            elif aspect_ratio == "21:9":
                coords = [-4.48, 2.69, -2.0, 1.0]
            else:
                coords = [-2.25, 0.75, -2.0, 1.0]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: -2|ab| + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real) + 1j*(2*abs(self.z.real*self.z.imag)+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class CelticHeart(Fractal):
    def __init__(self, filename="celticHeart.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Celtic Heart")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-2.22, 1.33, -1.0, 1.0]
            elif aspect_ratio == "21:9":
                coords = [-2.99, 1.79, -1.0, 1.0]
            else:
                coords = [-1.65, 0.35, -1.0, 1.0]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: 2b|a| + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real) + 1j*(2*abs(self.z.real)*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class PerpendicularBuffalo(Fractal):
    def __init__(self, filename="perpendicularBuffalo.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print("Perpendicular Buffalo")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-3.33, 2.0, -1.5, 1.5]
            elif aspect_ratio == "21:9":
                coords = [-4.48, 2.69, -1.5, 1.5]
            else:
                coords = [-2.25, 0.75, -1.5, 1.5]

        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: -2a|b| + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real) + 1j*(2*abs(self.z.imag)*self.z.real+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class Julia(Fractal):
    def __init__(self, real, img, filename="julia.bmp", color_map=None, max_iterations=250, aspect_ratio="16:9", xdim=480, coords=None, escape_radius=4):
        print(f"Julia Set ({real} + {img}i)")
        if coords == None:
            if aspect_ratio == "16:9":
                coords=[-2.67, 2.67, -1.5, 1.5]
            elif aspect_ratio == "21:9":
                coords = [-3.58, 3.58, -1.5, 1.5]
            else:
                coords = [-1.5, 1.5, -1.5, 1.5]

        c = real+1j*img
        super().__init__(*coords, filename, color_map, max_iterations, aspect_ratio, xdim, escape_radius)
        self.z = self.X+1j*self.Y
        self.c = np.full((self.dimen_y, self.dimen_x), c, dtype=np.complex128)
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), self.filename)

    def __gen_points(self):
        for _ in range(self.iterations):
            # z_(n+1) = (z_n)^2 + c
            self.z = z = np.where(self.is_not_diverged, self.z**2 + self.c, self.z)
            self._update_img_data()
        return self._get_colors()


def showColormaps():
    tmp = Fractal(0,0,0,0,"")
    cm = tmp.color_maps
    count = 1
    print("Available color maps:")
    print("\t", end="")
    for c in cm:
        if count%5 == 0:
            print(c, end="\n")
            print("\t", end="")
        else:
            print(c, end=", ")
        count+=1
    print("")

def showClasses():
    count = 1
    print("Available classes:")
    print("\t", end="")
    for name, _ in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if count%3 == 0:
            print(name, end="\n")
            print("\t", end="")
        else:
            print(name, end=", ")
        count+=1
    print("")

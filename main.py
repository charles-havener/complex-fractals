from PIL import Image
import numpy as np

#TODO: inspect all images and to adjust for centered
#TODO: celtic 90deg rotation?


class Fractal():
    def __init__(self, min_x, max_x, min_y, max_y, color_map=None, R=4):
        # 2560,1440; 1920,1080; 960,540; 480,270 
        self.dimen_x, self.dimen_y = 960, 540
        self.iterations = 510
        self.R = R

        self.X = self.__setX(min_x, max_x, self.dimen_x)
        self.Y = self.__setY(min_y, max_y, self.dimen_y)

        self.img_data = np.zeros((self.dimen_y, self.dimen_x), dtype=np.float32)
        self.is_not_diverged = np.ones((self.dimen_y, self.dimen_x), dtype=np.float32)

        self.__set_color_maps()
        self.cm = self.color_maps["pink-teal"] if color_map is None else self.color_maps[color_map]
        #print(f"  -iterating points")

    def set_dimensions(self, x, y):
        self.dimen_x = x
        self.dimen_y = y

    def set_iterations(self, iterations):
        self.iterations = iterations

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
            "green-purple": [0.00, 0.00, 0.00, 4.00, 1.00, 2.50, 1.00, 3.00, 1.50],
            
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
    def __init__(self, color_map=None, R=4):
        #print("Mandelbrot")
        super().__init__(-3.33, 2.0, -1.5, 1.5, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "mandelbrot.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: 2ab + Im(c)
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real)+1j*(2*self.z.real*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class Mandelbar(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Mandelbar")
        super().__init__(-1.78, 1.78, -1, 1, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "mandelbar.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: -2ab + Im(c)
            self.z = z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real)+1j*(-2*self.z.real*self.z.imag+self.c.imag) + self.c, self.z)
            self._update_img_data()
        return self._get_colors()


class PerpendicularMandelbrot(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Perpendicular Mandelbrot")
        super().__init__(-3.0, 2.33, -1.5, 1.5, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "perpendicularMandelbrot.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: -2b|a| + Im(c)
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real)+1j*(-2*self.z.imag*abs(self.z.real)+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class Celtic(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Celtic")
        super().__init__(-4.12, 3.0, -2, 2, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "celtic.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: 2ab + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real)+1j*(2*self.z.real*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class CelticMandelbar(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Celtic Mandelbar")
        super().__init__(-3.33, 2.0, -1.5, 1.5, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "celticMandelbar.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: -2ab + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real)+1j*(-2*self.z.real*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class PerpendicularCeltic(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Perpendicular Celtic)
        super().__init__(-3.33, 2.0, -1.5, 1.5, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "perpendicularCeltic.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: -2b|a| + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real)+1j*(-2*abs(self.z.real)*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class BurningShip(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Burning Ship")
        super().__init__(-3.0, 2.33, -2.0, 1.0, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "burningShip.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: -2|ab|
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real) + 1j*(2*abs(self.z.imag*self.z.real) + self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class HeartMandelbrot(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Heart Mandelbrot)
        super().__init__(-2.22, 1.33, -1, 1, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "heartMandelbrot.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: 2b|a| + Im(c)
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real) + 1j*(2*self.z.imag*abs(self.z.real)+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class PerpendicularBurningShip(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Perpendicular Burning Ship")
        super().__init__(-3.0, 2.33, -1.5, 1.5, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "perpendicularBurningShip.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: a^2 - b^2 + Re(c)
            # Im: -2a|b| + Im(c)
            self.z = np.where(self.is_not_diverged, (self.z.real**2 - self.z.imag**2 + self.c.real) + 1j*(2*self.z.real*abs(self.z.imag)+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class Buffalo(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Buffalo")
        super().__init__(-3.33, 2.0, -2.0, 1.0, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "buffalo.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: -2|ab| + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real) + 1j*(2*abs(self.z.real*self.z.imag)+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class CelticHeart(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Celtic Heart)
        super().__init__(-2.22, 1.33, -1.0, 1.0, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "celticHeart.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: 2b|a| + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real) + 1j*(2*abs(self.z.real)*self.z.imag+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()


class PerpendicularBuffalo(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Perpendicular Buffalo")
        super().__init__(-3.33, 2.0, -1.5, 1.5, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "perpendicularBuffalo.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # Re: |a^2 - b^2| + Re(c)
            # Im: -2a|b| + Im(c)
            self.z = np.where(self.is_not_diverged, (abs(self.z.real**2 - self.z.imag**2) + self.c.real) + 1j*(2*abs(self.z.imag)*self.z.real+self.c.imag), self.z)
            self._update_img_data()
        return self._get_colors()





class Julia(Fractal):
    def __init__(self, real, img, color_map=None, R=4):
        #print("Julia Set")
        c = real+1j*img
        super().__init__(-2.67, 2.67, -1.5, 1.5, color_map, R)
        self.z = self.X+1j*self.Y
        self.c = np.full((self.dimen_y, self.dimen_x), c, dtype=np.complex128)
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "julia.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # z_(n+1) = (z_n)^2 + c
            self.z = z = np.where(self.is_not_diverged, self.z**2 + self.c, self.z)
            self._update_img_data()
        return self._get_colors()





# ------------------------------ Misc


#TODO: fix denominator 0 in some cases
class Nova(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Nova")
        super().__init__(-3.33, 5.55, -2.5, 2.5, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "nova.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # z_(n+1) = ...
            self.z = z = np.where(self.is_not_diverged, self.z - ((self.z - 1)**3)/(3*self.z**2) + self.c, self.z)
            self._update_img_data()
        return self._get_colors()


class Magnet(Fractal):
    def __init__(self, color_map=None, R=4):
        #print("Magnet")
        super().__init__(-3.33, 5.55, -2.5, 2.5, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "magnet.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # z_(n+1) = ...
            self.z = z = np.where(self.is_not_diverged, ((self.z**2+self.c-1)/(2*self.z+self.c-2))**2, self.z)
            self._update_img_data()
        return self._get_colors()


if __name__ == "__main__":

    '''
    cm = ["blue-sepia","green-purple","pink-teal","orange-blue","indigo-green","green-purple","black-white","white-black","purple","orange","cyan","blue","lime","pink","seablue","green","watermelon","red","indigo","shamrock", "barbour","wine","midnightblue","yellow","magenta","teal"]

    for c in cm:
        print(c)
        Mandelbrot(c)
        BurningShip(c)
        Julia(0.285, 0.01, c)
    '''
    Celtic("black-white")
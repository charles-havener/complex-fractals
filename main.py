from PIL import Image
import numpy as np

# Flow
#? blue->sepia [0,0,0], [v**4, v**2.5, v**1], [v**1, v**1.5, v**3]
#? green->purple [0,0,0], [v**2.5, v**1, v**4], [v**1.5, v**3, v**1]
#? pink->teal [0, 0, 0,], [v**1, v**4, v**2.5], [v**3, v**1, v**1.5]

#? orange->blue [0, 0, 0], [v**1, v**2.5, v**4], [v**3, v**1.5, v**1]
#? indigo->green [0,0,0], [v**2.5, v**4, v**1], [v**1.5, v**1, v**3]
#? green->purple [0,0,0], [v**4, v**1, v**2.5], [v**1, v**3, v**1.5]

# Black/White
#? black->white** := [0,0,0], [v**10, v**10, v**10], [v,v,v]
#? white->black** := [0,0,0], [v**1, v**1, v**1], [v**2, v**2, v**2]

# Single
#? purple** [0.5, 0, 1], [v**1.5, v**4, v**1], [v**1.2, v**1.8, v**1]
#? orange** [1, 0.5, 0], [v**1, v**1.5, v**4], [v**1, v**1.2, v**1.8]
#? cyan** [0, 1, 0.5], [v**4, v**1, v**1.5], [v**1.8, v**1, v**1.2]

#? blue** [0, 0.5, 1], [v**4, v**1.5, v**1], [v**1.8, v**1.2, v**1]
#? lime** [0.5, 1, 0], [v**1.5, v**1, v**4], [v**1.2, v**1, v**1.8]
#? pink** [1, 0, 0.5], [v**1, v**4, v**1.5], [v**1, v**1.8, v**1.2]

#? blue** [0, 0.22, 1], [v**4, v**2.9, v**1], [v**1.8, v**1.7, v**1]
#? green** [0.22, 1, 0], [v**2.9, v**1, v**4], [v**1.7, v**1, v**1.8]
#? watermelon** [1, 0, 0.22], [v**1, v**4, v**2.9], [v**1, v**1.8, v**1.7]

#? red** [1, 0.22, 0], [v**1, v**2.9, v**4], [v**1, v**1.7, v**1.8]
#? indigo** [0.22, 0, 1], [v**2.9, v**4, v**1], [v**1.7, v**1.8, v**1]
#? shamrock** [0, 1, 0.22], [v**4, v**1, v**2.9], [v**1.8, v**1, v**1.7]

#? barbour [0.04, 0.39, 0.08], v**3, v**1.5, v**3], [v**1.4, v**1.1, v**1.4]
#? wine [0.39, 0.08, 0.04], [v**1.5, v**3, v**3], [v**1.1, v**1.4, v**1.4]
#? midnightblue [0.08, 0.04, 0.39], [v**3, v**3, v**1.5], [v**1.4, v**1.4, v**1.1]

#? yellow [.7, .7, .2], [v**1, v**1, v**3], [v**1, v**1, v**1.8]
#? magenta [0.7, 0.2, 0.7], [v**1, v**3, v**1], [v**1, v**1.8, v**1]
#? teal [0.2, 0.7, 0.7], [v**3, v**1, v**1], [v**1.8, v**1, v**1]

class Fractal():
    def __init__(self, min_x, max_x, min_y, max_y, color_map=None, R=4):
        self.dimen_x, self.dimen_y = 960, 540
        self.iterations = 255
        self.R = R
        self.color_map = color_map
        
        self.X = self.__setX(min_x, max_x, self.dimen_x)
        self.Y = self.__setY(min_y, max_y, self.dimen_y)

        self.img_data = np.zeros((self.dimen_y, self.dimen_x), dtype=np.float32)
        self.is_not_diverged = np.ones((self.dimen_y, self.dimen_x), dtype=np.float32)

        print(f"  -iterating points")

        '''
        TODO: R not an argument, defaults to 4 w/ method to set R
        TODO: pass in width and height as args or pass in an image object with width and height?
        TODO: add dictionary of color maps {cmap_name: [a,b,c,d,e,f,g,h,i]}
            - idx are in order for numbers as the appear
        '''

    def set_dimensions(self, x, y):
        self.dimen_x = x
        self.dimen_y = y

    def set_iterations(self, iterations):
        self.iterations = iterations

    def __setX(self, a, b, dimen):
        return np.linspace(a, b, dimen).reshape((1, dimen))
    
    def __setY(self, a, b, dimen):
        return np.linspace(a, b, dimen).reshape((dimen, 1))
    
    @staticmethod
    def color(z, i, R):
        if abs(z) < R:
            return 0, 0, 0
        v = np.log2(i + R - np.log2(np.log2(abs(z)))) / 5
        if v < 1.0:
            return v**1, v**4, v**2.5 # outer
        else:
            v = max(0, 2 - v)
            return v**3, v**1, v**1.5 # inner

    def _get_colors(self):
        print("  -assigning colors")
        r, g, b = np.frompyfunc(self.color, 3, 3)(self.z, self.img_data, self.R)
        img_c = np.dstack((r,g,b))
        return np.uint8(img_c * 255)

    def _update_img_data(self):
        self.is_not_diverged = (np.abs(self.z)<self.R).astype(np.float32) #0->diverged, 1->not
        self.img_data += self.is_not_diverged

    def _create_image(self, color_array, filename):
        print("  -creating images")
        display = Image.fromarray(color_array, 'RGB')
        display.save(filename)


class BurningShip(Fractal):
    def __init__(self, color_map=None, R=4):
        print("Burning Ship")
        super().__init__(-3.0, 2.33, -2.0, 1.0, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "burning.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # z_(n+1) = (|Re(z_n)| + i|Im(z_n)|)^2 + c
            self.z = np.where(self.is_not_diverged, (abs(self.z.real)+abs(self.z.imag)*1j)**2 + self.c, self.z)
            self._update_img_data()
        return self._get_colors()


class Mandelbrot(Fractal):
    def __init__(self, color_map=None, R=4):
        print("Mandelbrot")
        super().__init__(-3.33, 2.0, -1.5, 1.5, color_map, R)
        self.z = np.zeros((self.dimen_y, self.dimen_x), dtype=np.complex128)
        self.c = self.X+1j*self.Y
        self.run()

    def run(self):
        self._create_image(self.__gen_points(), "mandelbrot.bmp")

    def __gen_points(self):
        for _ in range(self.iterations):
            # z_(n+1) = (z_n)^2 + c
            self.z = z = np.where(self.is_not_diverged, self.z**2 + self.c, self.z)
            self._update_img_data()
        return self._get_colors()


class Julia(Fractal):
    def __init__(self, real, img, color_map=None, R=4):
        print("Julia Set")
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

if __name__ == "__main__":
    #BurningShip()
    #Mandelbrot()
    Julia(0.285, 0.01)
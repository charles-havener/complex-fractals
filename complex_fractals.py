from PIL import Image
import numpy as np
import math
from numba import cuda, jit
from fractal_types import f_type_identifiers, f_type_parameters


#Todo: add identifer "list", which would ouput a list of all identifier options
#Todo: create actual gif/mp4 file, rather than saving a series of images

'''
Identifiers (since passing strings to gpu was causing issues):
Indexed based on order added
0 -> Mandelbrot
1 -> Mandelbar
2 -> PerpendicularMandelbrot
3 -> CelticMandelbrot
4 -> CelticMandelbar
5 -> PerpendicularCeltic
6 -> BurningShip
7 -> HeartMandelbrot
8 -> PerpendicularBurningShip
9 -> Buffalo
10 -> HeartCeltic
11 -> PerpendicularBuffalo
'''

@jit
def color(matri, smooth_iter, stripe_avg, stripe_density, stripe_memory, blend_factor, cm, cycle_count):
    """Deterimine the final color assigned to pixels in the output image.

    Args:
        matri (list): the (real,imaginary) location in the matrix to overide the RGB value of.
        smooth_iter (float): the smooth iteration count of the pixel.
        stripe_avg (float): the stripe value assigned to the pixel.
        stripe_density (int): how dense the stripes are in the final image.
        stripe_memory (float): the weight of historical values kept between iterations.
        blend_factor (float): how strong of a showing the stripes make in the final image, value in [0,1].
        cm (ColorMap.colormap): the colormap used to color the fractal.
        cycle_count (int): the number of iterations before the colormap cycles back to the start.
    """

    # Custom mixing. Gives nicer results than 50% mix.
    def blend(i, a, blend_factor):
        """Mixes a channel of the smooth iteration count color (i) with the branching value (a) of
        the coordinate.

        Args:
            i (float): a channel value assigned to the smooth iteration, value in [0,1].
            a (float): value of the stripe_avg for the point, value in [0,1].
            blend_factor (float): how strong of a showing the stripes make in the final image, value in [0,1].

        Returns:
            float: the mixed channel value for the pixel
        """
        if 2*a < 1:
            o = 2*i*a
        else:
            o = 1 - 2*(1-i)*(1-a)
        return o*blend_factor + i*(1-blend_factor)

    # Power transform and map to [0,1]
    smooth_iter = math.sqrt(smooth_iter)%cycle_count/cycle_count
    col = round(smooth_iter*(cm.shape[0]-1))

    # Assign value to each channel
    for i in range(3):
        matri[i] = cm[col, i]
        if stripe_avg>0 and stripe_memory>0:
            matri[i] = blend(matri[i], stripe_avg, blend_factor)
        matri[i] = max(0, min(1, matri[i])) # Enusure [0,1]

@jit
def smooth_iter(c, iter_max, stripe_density, stripe_memory, identifier=0):
    """Determine the smooth iteration count value of the pixel and the value of it's addend function.

    Args:
        c (complex): a value used in the iteration function of the fractal. Serves a different purpose for differnt fractals.
        iter_max (int): maximum number of iterations until a point that doesn't escape is considered part of the set
        stripe_density (int): how dense the stripes are in the final image
        stripe_memory (float): the weight of historical values kept between iterations
        identifier (int, optional): unique id used to determine iteration function. Defaults to 0.

    Returns:
        tuple of floats: the smooth iteration count, and the stripe_avg value
    """
    escape_radius_squared = 10**10
    z = complex(0,0)

    # Flag to only compute stripe values if relevant params are non-zero
    stripe = stripe_density>0 and stripe_memory>0
    stripe_avg = 0 # holds average of addend function value

    for n in range(iter_max):
        if identifier == 0: # Mandelbrot
            z = (z.real**2 - z.imag**2 + c.real)+1j*(2*z.real*z.imag+c.imag)
        elif identifier == 1: # Mandelbar
            z = (z.real**2 - z.imag**2 + c.real)+1j*(-2*z.real*z.imag+c.imag)
        elif identifier == 2: # PerpendicularMandelbrot
            z = (z.real**2 - z.imag**2 + c.real)+1j*(-2*z.imag*abs(z.real)+c.imag)
        elif identifier == 3: # CelticMandelbrot
            z = (abs(z.real**2 - z.imag**2) + c.real)+1j*(2*z.real*z.imag+c.imag)
        elif identifier == 4: # CelticMandelbar
            z = (abs(z.real**2 - z.imag**2) + c.real)+1j*(-2*z.real*z.imag+c.imag)
        elif identifier == 5: # PerpendicularCeltic
            z = (abs(z.real**2 - z.imag**2) + c.real)+1j*(-2*abs(z.real)*z.imag+c.imag)
        elif identifier == 6: # BurningShip
            z = (z.real**2 - z.imag**2 + c.real) + 1j*(-2*abs(z.imag*z.real) + c.imag)
        elif identifier == 7: # HeartMandelbrot
            z = (z.real**2 - z.imag**2 + c.real) + 1j*(2*z.imag*abs(z.real)+c.imag)
        elif identifier == 8: # PerpendicularBurningShip
            z = (z.real**2 - z.imag**2 + c.real) + 1j*(-2*z.real*abs(z.imag)+c.imag)
        elif identifier == 9: # Buffalo
            z = (abs(z.real**2 - z.imag**2) + c.real) + 1j*(-2*abs(z.real*z.imag)+c.imag)
        elif identifier == 10: # HeartCeltic
            z = (abs(z.real**2 - z.imag**2) + c.real) + 1j*(2*abs(z.real)*z.imag+c.imag)
        elif identifier == 11: # PerpendicularBuffalo
            z = (abs(z.real**2 - z.imag**2) + c.real) + 1j*(2*abs(z.imag)*z.real+c.imag)

        # calculate addend
        if stripe:
            addend = (math.cos(stripe_density*math.atan2(z.imag, z.real))+1)/2 # Cos is symmetrical
            #addend = (math.sin(stripe_density*math.atan2(z.imag, z.real))+1)/2 # Sin used in paper
        
        # Check for escape
        if z.real*z.real + z.imag*z.imag > escape_radius_squared:
            modz = abs(z)
            factor = math.log(escape_radius_squared)/(2*math.log(modz))
            smooth = 1 + math.log(factor)/math.log(2)
            
            if stripe:
                stripe_avg = (stripe_avg*(1+smooth*(stripe_memory-1))+addend*smooth*(1-stripe_memory))

            return (n+smooth, stripe_avg)
        
        if stripe:
            stripe_avg = stripe_avg*stripe_memory + addend*(1-stripe_memory)
        
    # Never escaping -> part of set and return 0s
    return (0,0)

@jit
def compute_set(real_range, imag_range, iter_max, cm, cycle_count, stripe_density, 
                stripe_memory, blend_factor, identifier):
    """Create the fractal image using the CPU. Much slower than the GPU version.

    Args:
        real_range (float): the range of the real axis.
        imag_range (float): the range of the imaginary axis.
        iter_max (int): maximum number of iterations until a point that doesn't escape is considered part of the set.
        cm (ColorMap.colormap): the colormap used to color the fractal.
        cycle_count (int): the number of iterations before the colormap cycles back to the start.
        stripe_density (int): how dense the stripes are in the final image.
        stripe_memory (float): the weight of historical values kept between iterations.
        blend_factor (float): how strong of a showing the stripes make in the final image, value in [0,1].
        identifier (int, optional): unique id used to determine iteration function.

    Returns:
        array: the RGB values of each pixel of the output image.
    """

    real_pixels = len(real_range)
    imag_pixels = len(imag_range)

    # Initialize output matrix
    mat = np.zeros((imag_pixels, real_pixels, 3))

    # Loop through matrix
    for r in range(real_pixels):
        for i in range(imag_pixels):
            c = complex(real_range[r], imag_range[i])
            smooth_i, stripe_avg = smooth_iter(c, iter_max, stripe_density, stripe_memory, identifier)
            if smooth_i > 0:
                color(mat[i,r,], smooth_i, stripe_avg, stripe_density, stripe_memory, 
                      blend_factor, cm, cycle_count)
    return mat

@cuda.jit
def compute_set_gpu(mat, real_min, real_max, imag_min, imag_max, iter_max, cm, 
                    cycle_count, stripe_density, stripe_memory, blend_factor, identifier):
    """Create the fractal image using the GPU to do the bulk of the work. Much faster than
    the CPU alternative. Required CUDA tookit for numba's cuda.jit to work.

    Args:
        mat (array): empty array of all pixels to store their RGB values for output.
        real_min (float): the minimum value of the real axis.
        real_max (float): the maximal value of the real axis.
        imag_min (float): the minimum value of the imaginary axis.
        imag_max (float): the maximal value of the imaginary axis.
        iter_max (int): maximum number of iterations until a point that doesn't escape is considered part of the set.
        cm (ColorMap.colormap): the colormap used to color the fractal.
        cycle_count (int): the number of iterations before the colormap cycles back to the start.
        stripe_density (int): how dense the stripes are in the final image.
        stripe_memory (float): the weight of historical values kept between iterations.
        blend_factor (float): how strong of a showing the stripes make in the final image, value in [0,1].
        identifier (int): unique id used to determine iteration function.
    """
    grid = cuda.grid(1)
    r,i = grid%mat.shape[1], grid//mat.shape[1]

    # Check boundaries
    if (i<mat.shape[0]) and (r<mat.shape[1]):
        real = real_min+r/(mat.shape[1]-1)*(real_max-real_min)
        imag = imag_min+i/(mat.shape[0]-1)*(imag_max-imag_min)
        c = complex(real, imag)
        smooth_i, stripe_avg = smooth_iter(c, iter_max, stripe_density, stripe_memory, identifier)
        if smooth_i > 0:
            color(mat[i,r,], smooth_i, stripe_avg, stripe_density, stripe_memory, blend_factor, cm, cycle_count)


class ColorMap:
    def __init__(self, rgb_phases=[0.0,0.8,0.15], ncol=2**12, random_phases=False):
        """Creation and viewing of color maps to be applied to fractals

        Args:
            rgb_phases (list of floats, optional): phases used to create cyclic color map. 
               Values in [0.0, 1.0]. Defaults to [0.0,0.8,0.15].
            ncol (int, optional): number of columns used in the color map. Higher values lead to 
                smoother transitions. Defaults to 2**12.
            random_phases (bool, optional): Whether random rgb_phases should be used. Will always 
                overide any values passed to rgb_phases if True. Defaults to False.
        """
        self.rgb_phases = rgb_phases
        self.ncol = ncol
        if random_phases: self.generate_random_rgb_phases()
        self.colormap = self.create_colormap()

    def create_colormap(self):
        """Generates and returns a colormap."""
        def colormap(v, rgb_phases):
            color_segs = np.column_stack(((v+rgb_phases[0])*2*math.pi,
                                          (v+rgb_phases[1])*2*math.pi,
                                          (v+rgb_phases[2])*2*math.pi))
            rgb_values = (0.5 + 0.5*np.sin(color_segs)) # [-1, 1] -> [0, 1]
            return rgb_values
        return colormap(np.linspace(0,1,self.ncol), self.rgb_phases)

    def preview_colormap(self):
        """Preview the colormap."""
        ncol = 2**12
        c = [self.create_colormap()*255]*(self.ncol//4)
        im = Image.fromarray(np.uint8(c)).convert('RGB')
        im.show()

    def generate_random_rgb_phases(self):
        """Generates 3 random phases to create a colormap."""
        self.rgb_phases = np.random.uniform(0,1,3)
        print(f"Random phases: [{','.join([str(p) for p in self.rgb_phases])}]")


class ComplexFractal:
    """The main class used to create fractals within the complex plane."""

    def __init__(self, identifier=0, width=480, aspect_ratio="16:9", cycle_count=16, oversample=2, 
        real=-0.3775, imag=0.0, zoom=1, rgb_phases=[0.0, 0.8, 0.15], random_phases=True, 
        iter_max=350, stripe_density=2, stripe_memory=0.9, blend_factor=1.0, gpu=False, filename=None):
        
        
        
        """The main class for creating fractals in the complex plane

        Args:
            identifier (int, optional): unique id used to determine iteration function. Defaults to 0.
            width (int, optional): the width of the image to be output. Defaults to 480.
            aspect_ratio (str, optional): The desired aspect ratio of the output image. Defaults to "16:9".
            cycle_count (int, optional): the number of iterations before the colormap cycles back to 
                the start. Defaults to 16.
            oversample (int, optional): scale the image my a factor of oversample to assign colors to the 
                passed resolution with pixel values being the average of oversample*oversample grids. 
                Defaults to 2.
            real (float, optional): the real value to focus on or to zoom in on. Defaults to -0.3775.
            imag (float, optional): the imaginary value to focus on or to zoom in on. Defaults to 0.0.
            zoom (int, optional): the depth of the zoom. >= 1. Defaults to 1.
            rgb_phases (list of floats, optional): phases used to create cyclic color map. 
               Values in [0.0, 1.0]. Defaults to [0.0,0.8,0.15].
            random_phases (bool, optional): Whether random rgb_phases should be used. Will always 
                overide any values passed to rgb_phases if True. Defaults to False.
            iter_max (int, optional): maximum number of iterations until a point that doesn't escape 
                is considered part of the set. Defaults to 350.
            stripe_density (int, optional): how dense the stripes are in the final image. Defaults to 2.
            stripe_memory (float, optional): the weight of historical values kept between iterations. 
                Defaults to 0.9.
            blend_factor (float): how strong of a showing the stripes make in the final image, value in [0,1].
            gpu (bool, optional): Compute with GPU or with CPU. True->GPU. Defaults to False.
            filename (str, optional): The name to be assigned to the output image. Defaults to None.
        """

        # Arguments that need validation
        self.width = width
        self.aspect_ratio = aspect_ratio
        self.cycle_count = cycle_count
        self.iter_max = iter_max
        self.oversample = oversample
        self.real=real
        self.imag=imag
        self.zoom = zoom
        self.rgb_phases = rgb_phases
        self.random_phases = random_phases
        self.iter_max = iter_max
        self.stripe_density = stripe_density
        self.stripe_memory = stripe_memory
        self.blend_factor = blend_factor
        self.gpu = gpu

        # Arguments of the fractal type
        self.identifier = f_type_identifiers[identifier.lower() if type(identifier) == str else identifier]
        
        # Help function to list out possible identifiers:
        self.__list_tyes() # only outputs when identifier is -1 or help

        self.center = f_type_parameters[self.identifier]["center"]
        self.im_range = f_type_parameters[self.identifier]["im_range"]
        self.filename = filename if type(filename) == str else f_type_parameters[self.identifier]["filename"]

        # Calculated variables
        self.re_range = self.__gen_re_range()
        self.real_pixels = round(self.width)
        self.imag_pixels = self.__gen_imag_pixels()

        # Setup the color map to be used
        self.cm = ColorMap(self.rgb_phases, random_phases=random_phases).colormap

    def __list_tyes(self):
        """lists possible values for identifiers in the console
        """
        if self.identifier==-1:
            for k in f_type_identifiers:
                if type(k) == str:
                    print(f"{str(f_type_identifiers[k]).rjust(2)} - {k}")
            exit()

    def __gen_re_range(self):
        """Determine range of real axis from aspect ratio and imag range.

        Returns:
            float: range of real axis.
        """
        ar = [int(v) for v in self.aspect_ratio.split(":")]
        return self.im_range*ar[0]/ar[1]

    def __gen_imag_pixels(self):
        """Determine number of pixels along imaginary axis from aspect ratio and
        number of pixels along real range.

        Returns:
            float: pixels of imaginary axis.
        """
        r = self.real_pixels
        ar = [int(v) for v in self.aspect_ratio.split(":")]
        return round(r*ar[1]/ar[0])

    def __gen_range_sizes(self):
        """Determine the complex plane range of the imaginary and real axes values
        for the desired zoom depth and aspect ratio.

        Returns:
            tuple of floats: the range of the real and imaginary axis.
        """
        ar = [int(v) for v in self.aspect_ratio.split(":")]
        imag_range_size = self.im_range/self.zoom
        real_range_size = imag_range_size*ar[0]/ar[1]
        return (real_range_size, imag_range_size)

    def __gen_bounds(self, real_range_size, imag_range_size):
        """Determine the upper bounds of the real and imaginary axes for the image to be drawn (lower
        bound is calculated from the maximum by subtracting the range). Focuses on staying near center 
        of the fractal. Mainly used for higer level zooms so more of the 'interesting' patterns remain 
        in view as opposed to the emptyness seen at points further from the center.

        Args:
            real_range_size (float): the size of the range of the real axis.
            imag_range_size (float): the size of the range of the imaginary axis.

        Returns:
            tuple of floats: the maximal values used in the real and imaginary axis. 
                Min is determined using the max and respective range.
        """
        real_shift = 0
        if self.center.real + self.re_range/2 < self.real + real_range_size/2:
            real_shift = (self.real + real_range_size/2) - (self.center.real + self.re_range/2)
        elif self.center.real - self.re_range/2 > self.real - real_range_size/2:
            real_shift = (self.real - real_range_size/2) - (self.center.real - self.re_range/2)
        real_max = self.real + real_range_size/2 - real_shift

        imag_shift = 0
        if self.center.imag + self.im_range/2 < self.imag + imag_range_size/2:
            imag_shift = (self.imag + imag_range_size/2) - (self.center.imag + self.im_range/2)
        elif self.center.imag - self.im_range/2 > self.imag - imag_range_size/2:
            imag_shift = (self.imag - imag_range_size/2) - (self.center.imag - self.im_range/2)
        imag_max = self.imag + imag_range_size/2 - imag_shift

        return (real_max, imag_max)

    def __gen_rec_iteration_count(self):
        """Not used, may be useful later as a possible addition for animate()."

        Returns:
            int : an iter_max value suitable for the zoom level.
        """
        factor = math.ceil(math.log(self.zoom)/math.log(2))
        rec_iter = max(250, factor*250)
        print(f"Using Recommended Iterations: {rec_iter}")
        return rec_iter

    def _create_set(self):
        """Generate the values of the set for all pixels based on parameters passed.
        Can compute with either GPU or CPU (GPU required CUDA, but is significantly faster).
        """

        # Power transform
        cycle_count = math.sqrt(self.cycle_count)

        # Apply oversampling (psuedo anti-aliasing)
        real_points = self.real_pixels*self.oversample
        imag_points = self.imag_pixels*self.oversample

        # Determine bounds in Complex plane
        real_range_size, imag_range_size = self.__gen_range_sizes()
        real_max, imag_max = self.__gen_bounds(real_range_size, imag_range_size)
        real_min = real_max-real_range_size
        imag_min = imag_max-imag_range_size

        # Create the set using GPU
        if self.gpu:
            self.set = np.zeros((imag_points, real_points, 3))
            pixel_count = real_points*imag_points
            num_threads = 32
            num_blocks = math.ceil(pixel_count/num_threads)
            
            compute_set_gpu[num_blocks, num_threads](self.set, real_min, real_max, imag_min, imag_max,
                self.iter_max, self.cm, self.cycle_count, self.stripe_density, self.stripe_memory, 
                self.blend_factor, self.identifier)

        # Create the set using CPU
        else:
            real_range = np.linspace(real_min, real_max, real_points)
            imag_range = np.linspace(imag_min, imag_max, imag_points)
            self.set = compute_set(real_range, imag_range, self.iter_max, self.cm, cycle_count, 
            self.stripe_density, self.stripe_memory, self.blend_factor, self.identifier)

        self.set = (255*self.set).astype(np.uint8)

        # Remove oversampling if present
        if self.oversample > 1:
            self.set = (self.set.reshape(
                (self.imag_pixels, self.oversample, self.real_pixels, self.oversample, 3))
                .mean(3).mean(1).astype(np.uint8))

    def draw(self):
        """Saves the image to the directory the file was ran from.
        """
        self._create_set()
        img = Image.fromarray(self.set[::-1,:,:], 'RGB')

        img.save(f"{self.filename}.jpg")

    def animate(self, start=1, end=2**10, rate=2):
        """Create a series of images, that when played in sequence create a zoom animation.

        Args:
            start (float): the initial zoom level (>=1).
            end (float): the target zoom level to be reached at the end (>= start).
            rate (float): the speed at which the zoom level approaches the end value (> 1.0).
        """

        images_to_create = math.floor(1+(math.log(end)-math.log(start))/math.log(rate))

        # save initial zoom value set to restore later
        zoom_store = self.zoom
        self.zoom = start
        for i in range(images_to_create):
            self._draw(filename=f"{self.filename}_{str(i).zfill(5)}")
            print(f"Created {i+1} of {images_to_create} ({(i+1)/images_to_create:.2%})")
            self.zoom *= rate
        self.zoom = zoom_store

if __name__ == "__main__":
   f = ComplexFractal(-1)

from PIL import Image
import numpy as np
import math
from numba import cuda, jit

#? Future features

#todo redo input scheme to be similar to plotly if possible?

#todo custom color maps? list of #FFFFFFs passed in and smoothly loops and interpolates between them (max 5?)

#todo add triangle inequality and curvature average coloring on top of stripe?

#todo add julia sets for each fractal. might need new compute sets functions to swap z,c
#todo and an additional class para bool julia, with args for the re,im coords for the julia set?


#? Improvements/changes before merge into main

#todo add in the other fractals below

#todo user input for g in overlay function (visibility of stripes coming through in final image) [stripe_weight?]

#todo rename of stripe_s and stripe_w, maybe also stripe_t and stripe_a in functions to be more descriptive
#todo a is average, t is addend (Jussi 4.1 Average Colorings)

#todo change overlay function name to blend, vars to smooth_iter, addend, and stripe_weight

#todo recreate readme with new images, and a showing of how hard to understand parameters effect output

#todo verify requirements are still correct

#todo update gitignore to ignore more image types
#todo could add folder called assets then after ignoring all image extensions
#todo add lines such as: 
#todo   !/assets/**/*.png,
#todo   !/assets/**/*.bmp,
#todo   !/assets/**/*.jpg, etc...

'''main.py

Identifiers (since passing strings to gpu was causing issues):
Indexed based on order added

0 -> Mandelbrot
(z.real**2 - z.imag**2 + c.real)+1j*(2*z.real*z.imag+c.imag)

#TODO add the following:

1 -> Mandelbar
(z.real**2 - z.imag**2 + c.real)+1j*(-2*z.real*z.imag+c.imag)

2 -> PerpendicularMandelbrot
(z.real**2 - z.imag**2 + c.real)+1j*(-2*z.imag*abs(z.real)+c.imag)

3 -> Celtic
(abs(z.real**2 - z.imag**2) + c.real)+1j*(2*z.real*z.imag+c.imag)

4 -> CelticMandelbar
(abs(z.real**2 - z.imag**2) + c.real)+1j*(-2*z.real*z.imag+c.imag)

5 -> PerpendicularCeltic
(abs(z.real**2 - z.imag**2) + c.real)+1j*(-2*abs(z.real)*z.imag+c.imag)

6 -> BurningShip
(z.real**2 - z.imag**2 + c.real) + 1j*(2*abs(z.imag*z.real) + c.imag)

7 -> HeartMandelbrot
(z.real**2 - z.imag**2 + c.real) + 1j*(2*z.imag*abs(z.real)+c.imag)

8 -> PerpendicularBurningShip
(z.real**2 - z.imag**2 + c.real) + 1j*(2*z.real*abs(z.imag)+c.imag)

9 -> Buffalo
(abs(z.real**2 - z.imag**2) + c.real) + 1j*(2*abs(z.real*z.imag)+c.imag)

10 -> HeartCeltic
(abs(z.real**2 - z.imag**2) + c.real) + 1j*(2*abs(z.real)*z.imag+c.imag)

11 -> PerpendicularBuffalo
(abs(z.real**2 - z.imag**2) + c.real) + 1j*(2*abs(z.imag)*z.real+c.imag)

'''

@jit
def color(matri, smooth_iter, stripe_a, stripe_s, stripe_w, cm, cycle_count):
    """[summary]

    Args:
        matri (list): the real,imaginary location in the matrix to overide the RGB value of
        smooth_iter (float): the smooth iteration count of the pixel
        stripe_a (float): the value of the addend function for the pixel
        stripe_s (int): the stripe density
        stripe_w (float): the weight of the historical orbit
        cm (ColorMap.colormap): the colormap used to color the fractal
        cycle_count (int): the number of iterations before the colormap cycles back to the start
    """

    # Custom mixing. Gives nicer results than 50% mix.
    def overlay(i, a, g):
        """Mixes a channel of the smooth iteration count color (i) with the branching value (a) of
        the coordinate.
        #todo add example images to github

        Args:
            i (float): a channel value assigned to the smooth iteration [0,1]
            a (float): value of the addend function for the point [0,1]
            g (float): gamma value, how far 'warped' from the second image the mixing is [0,1]

        Returns:
            float: the mixed channel value for the pixel
        """
        if 2*a < 1:
            o = 2*i*a
        else:
            o = 1 - 2*(1-i)*(1-a)
        return o*g + i*(1-g)

    # Power transform and map to [0,1]
    smooth_iter = math.sqrt(smooth_iter)%cycle_count/cycle_count
    col = round(smooth_iter*(cm.shape[0]-1))

    # Assign value to each channel
    for i in range(3):
        matri[i] = cm[col, i]
        if stripe_a>0 and stripe_w>0:
            matri[i] = overlay(matri[i], stripe_a, 1)
        matri[i] = max(0, min(1, matri[i])) # Enusure [0,1]

@jit
def smooth_iter(c, iter_max, stripe_s, stripe_w, identifier=0):
    """Determine the smooth iteration count value of the pixel and the value of it's addend function.

    Args:
        c (complex): a value used in the iteration function of the fractal. Serves a different purpose for differnt fractals.
        iter_max (int): maximum number of iterations to run through to determine if a point is part of the set
        stripe_s (int): the density of stripes
        stripe_w (float): memory parameter of historical orbit
        identifier (int, optional): unique id of the calling class, used to determine iteration function. Defaults to 0.

    Returns:
        tuple, floats: the smooth iteration count, and the value of the addend function
    """
    escape_radius_squared = 10**10
    z = complex(0,0)

    # Flag to only compute stripe values if relevant params are non-zero
    stripe = stripe_s>0 and stripe_w>0
    stripe_a = 0 # holds addend function value

    for n in range(iter_max):
        if identifier == 0: # Mandelbrot
            z = (z.real**2 - z.imag**2 + c.real)+1j*(2*z.real*z.imag+c.imag)

        # calculate addend
        if stripe:
            stripe_t = (math.cos(stripe_s*math.atan2(z.imag, z.real))+1)/2 # Cos is symmetrical
            #stripe_t = (math.sin(stripe_s*math.atan2(z.imag, z.real))+1)/2 # Sin used in paper
        
        # Check for escape
        if z.real*z.real + z.imag*z.imag > escape_radius_squared:
            modz = abs(z)
            factor = math.log(escape_radius_squared)/(2*math.log(modz))
            smooth = 1 + math.log(factor)/math.log(2)
            
            if stripe:
                stripe_a = (stripe_a*(1+smooth*(stripe_w-1))+stripe_t*smooth*(1-stripe_w))

            return (n+smooth, stripe_a)
        
        if stripe:
            stripe_a = stripe_a*stripe_w + stripe_t*(1-stripe_w)
        
    # Never escaping -> part of set and return 0s
    return (0,0)

@jit
def compute_set(real_range, imag_range, iter_max, cm, cycle_count, stripe_s, stripe_w, identifier):
    """Create the fractal image using the CPU. Much slower than the GPU version.

    Args:
        real_range (float): the range of the real axis
        imag_range (float): the range of the imaginary axis
        iter_max (int): the maximum number of iterations to run through before concluding a point 
            is an element of the set.
        cm (ColorMap.colormap): the colormap to be used when coloring the set
        cycle_count (int): the number of iterations before the color map cycles back to the 
            beginning. Higher values lead to slower transitions between colors.
        stripe_s (int): Can be thought of as the density of stripes in the output. Should be >= 0
        stripe_w (float): The weight of the past addend function value to be carried forward 
            through the iterations. A memeory parameter of the orbital history.

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
            smooth_i, stripe_a = smooth_iter(c, iter_max, stripe_s, stripe_w, identifier)
            if smooth_i > 0:
                color(mat[i,r,], smooth_i, stripe_a, stripe_s, stripe_w, cm, cycle_count)
    return mat

@cuda.jit
def compute_set_gpu(mat, real_min, real_max, imag_min, imag_max, iter_max, cm, 
                    cycle_count, stripe_s, stripe_w, identifier):
    """Create the fractal image using the GPU to do the bulk of the work. Much faster than
    the CPU alternative. Required CUDA tookit for numba's cuda.jit to work.

    Args:
        mat (array): empty array of all pixels to store their RGB values for output
        real_min (float): the minimum value of the real axis
        real_max (float): the maximal value of the real axis
        imag_min (float): the minimum value of the imaginary axis
        imag_max (float): the maximal value of the imaginary axis
        iter_max (int): the maximum number of iterations to run through, before concluding a point
            is an element of the set.
        cm (ColorMap.colormap): the colormap to be used when coloring the set
        cycle_count (int): the number of iterations before the color map cycles back to the 
            beginning. Higher values lead to slower transitions between colors.
        stripe_s (int): Can be thought of as the density of stripes in the output. Should be >= 0.
        stripe_w (float): The weight of the past addend function value to be carried forward 
            through the iterations. A memory parameter of the orbital history.
        identifier (int): the unique value assigned to the calling class
    """
    grid = cuda.grid(1)
    r,i = grid%mat.shape[1], grid//mat.shape[1]

    # Check boundaries
    if (i<mat.shape[0]) and (r<mat.shape[1]):
        real = real_min+r/(mat.shape[1]-1)*(real_max-real_min)
        imag = imag_min+i/(mat.shape[0]-1)*(imag_max-imag_min)
        c = complex(real, imag)
        smooth_i, stripe_a = smooth_iter(c, iter_max, stripe_s, stripe_w, identifier)
        if smooth_i > 0:
            color(mat[i,r,], smooth_i, stripe_a, stripe_s, stripe_w, cm, cycle_count)


class ColorMap:
    def __init__(self, rgb_phases=[0.0,0.8,0.15], ncol=2**12, random_phases=False):
        """Creation and viewing of color maps to be applied to fractals

        Args:
            rgb_phases (list, floats, optional): phases used to create cyclic color map. 
                Each value should be in [0.0, 1.0], but others will still work. 
                Defaults to [0.0,0.8,0.15].
            ncol (int, optional): number of columns used in the  color map Higher values lead to 
                smoother transitions. Defaults to 2**12.
            random_phases (bool, optional): Wether random rgb_phases should be used. Will always 
                overide any values passed to rgb_phases if True. Defaults to False.
        """
        self.rgb_phases = rgb_phases
        self.ncol = ncol
        if random_phases: self.generate_random_rgb_phases()
        self.colormap = self.create_colormap()

    def create_colormap(self):
        """Generates and returns a colormap"""
        def colormap(v, rgb_phases):
            color_segs = np.column_stack(((v+rgb_phases[0])*2*math.pi,
                                          (v+rgb_phases[1])*2*math.pi,
                                          (v+rgb_phases[2])*2*math.pi))
            rgb_values = (0.5 + 0.5*np.sin(color_segs)) # [-1, 1] -> [0, 1]
            return rgb_values
        return colormap(np.linspace(0,1,self.ncol), self.rgb_phases)

    def preview_colormap(self):
        """Preview the colormap"""
        ncol = 2**12
        c = [self.create_colormap()*255]*(self.ncol//4)
        im = Image.fromarray(np.uint8(c)).convert('RGB')
        im.show()

    def generate_random_rgb_phases(self):
        """Generates 3 random phases to create a colormap"""
        self.rgb_phases = np.random.uniform(0,1,3)
        print(f"Random phases: [{','.join([str(p) for p in self.rgb_phases])}]")


class ComplexFractal:
    """The main class used to create fractals within the complex plane."""

    def __init__(self, im_range, center, identifier, width=1920, aspect_ratio="16:9", cycle_count=16,
        oversample=2, real=-0.3775, imag=0.0, zoom=1, rgb_phases=[0.0, 0.8, 0.15], random_phases=False, 
        iter_max=350, stripe_s=2, stripe_w=.9, gpu=False):
        """The main class for creating fractals in the complex plane

        Args:
            im_range (float): the range of the imaginary axis of the fractal. Passed from subclass.
            center (complex): the center point of the fractal. Passed from subclass
            identifier (int): the unique id of the subclass. Passed from subclass
            width (int, optional): the width of the image to be outpu. Defaults to 1920.
            aspect_ratio (str, optional): The desired aspect ratio of the outpu image. Defaults to "16:9".
            cycle_count (int, optional): Number of iterations before cycling back to the start of the colormap. Defaults to 16.
            oversample (int, optional): create a larger and scale down by averaging blocks, pseudo anti-aliasing. Defaults to 2.
            real (float, optional): the real value to focus on or to zoom in on. Defaults to -0.3775.
            imag (float, optional): the imaginary value to focus on or to zoom in on. Defaults to 0.0.
            zoom (int, optional): the depth of the zoom. >= 1. Defaults to 1.
            rgb_phases (list, optional): the phase of each channel in the cyclic color map to be created. Defaults to [0.0, 0.8, 0.15].
            random_phases (bool, optional): Use a random colormap. If true, overrides any passed rgb_phases. Defaults to False.
            iter_max (int, optional): Maximum number of iterations to run through before deciding a point is part of the set. Defaults to 350.
            stripe_s (int, optional): The density of the stripes. 0 for no stripes. Defaults to 2.
            stripe_w (float, optional): The weight of the historical orbit on the final value of the addend function. Defaults to .9.
            gpu (bool, optional): Compute with GPU or with CPU. True->GPU. Defaults to False.
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
        self.stripe_s = stripe_s
        self.stripe_w = stripe_w
        self.gpu = gpu

        # Arguments from subclass
        self.identifier = identifier
        self.center = center
        self.im_range = im_range

        # Calculated variables
        self.re_range = self.__gen_re_range()
        self.real_pixels = round(self.width)
        self.imag_pixels = self.__gen_imag_pixels()

        # Setup the color map to be used
        self.cm = ColorMap(self.rgb_phases, random_phases=random_phases).colormap

    def __gen_re_range(self):
        """Determine range of real axis from aspect ratio and imag range.

        Returns:
            float: range of real axis
        """
        ar = [int(v) for v in self.aspect_ratio.split(":")]
        return self.im_range*ar[0]/ar[1]

    def __gen_imag_pixels(self):
        """Determine number of pixels along imaginary axis from aspect ratio and
        number of pixels along real range.

        Returns:
            float: pixels of imaginary axis
        """
        r = self.real_pixels
        ar = [int(v) for v in self.aspect_ratio.split(":")]
        return round(r*ar[1]/ar[0])

    def __gen_range_sizes(self):
        """Determine the complex plane range of the imaginary and real axes values
        for the desired zoom depth and aspect ratio.

        Returns:
            tuple of floats: the range of the real and imaginary axis
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
            real_range_size (float): the size of the range of the real axis
            imag_range_size (float): the size of the range of the imaginary axis

        Returns:
            tuple of floats: [description]
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
        """Not used, possible addition later."
        Returns:
            int : an iter_max value suitable for the zoom level
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
                self.iter_max, self.cm, self.cycle_count, self.stripe_s, self.stripe_w, self.identifier)

        # Create the set using CPU
        else:
            real_range = np.linspace(real_min, real_max, real_points)
            imag_range = np.linspace(imag_min, imag_max, imag_points)
            self.set = compute_set(real_range, imag_range, self.iter_max, self.cm,
                cycle_count, self.stripe_s, self.stripe_w, self.identifier)

        self.set = (255*self.set).astype(np.uint8)

        # Remove oversampling if present
        if self.oversample > 1:
            self.set = (self.set.reshape(
                (self.imag_pixels, self.oversample, self.real_pixels, self.oversample, 3))
                .mean(3).mean(1).astype(np.uint8))

    def _draw(self, filename="output"):
        """Saves the image to the directory the file was ran from.

        Args:
            filename (str, optional): the name of the file to be saved. Defaults to "output".
        """
        self._create_set()
        img = Image.fromarray(self.set[::-1,:,:], 'RGB')

        img.save(f"{filename}.jpg")

    def _animate(self, start, end, rate, filename="anim"):
        """Create a series of images, that when played in sequence create a zoom animation

        Args:
            start (float): the initial zoom level (>=1)
            end (float): the target zoom level to be reached at the end
            rate (float): the speed at which the zoom level approaches the end value
            filename (str, optional): prefix of the image filenames. '_####' will be appended to the 
                end to keep sequence in order. Defaults to "anim".
        """

        images_to_create = math.floor(1+(math.log(end)-math.log(start))/math.log(rate))

        # save initial zoom value set to restore later
        zoom_store = self.zoom
        self.zoom = start
        for i in range(images_to_create):
            self._draw(filename=f"{filename}_{str(i).zfill(5)}")
            print(f"Created {i+1} of {images_to_create} ({(i+1)/images_to_create:.2%})")
            self.zoom *= rate
        self.zoom = zoom_store


class Mandelbrot(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_s=2, stripe_w=.9, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 2.5

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.3775, 0.0)

        # Unique identifier for this fractal type
        identifier = 0

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="mandelbrot"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="mandelbrot_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)


if __name__ == "__main__":
    real = -1.749705768080503
    imag = 6.13369029080495e-05
    f = Mandelbrot(stripe_s=2, rgb_phases=[0.5415155184227949,0.26203459358292536,0.1305322686383903],
         width=340, zoom=2**2, real=real, imag=imag, iter_max=600, random_phases=False, gpu=False,
         oversample=3, aspect_ratio="16:9", cycle_count=50, stripe_w=0.9)
    f.draw()
    #f.animate(end=2**45, rate=1.1)

    #c = ColorMap(random_phases=True)
    #c.preview_colormap()

    '''
    real = -1.749705768080503
    imag = 6.13369029080495e-05
    f = Mandelbrot(stripe_s=5, rgb_phases=[.8, .8, .8],
         width=6880, zoom=2**35.50, real=real, imag=imag, iter_max=20000, random_phases=False, gpu=True,
         oversample=3, aspect_ratio="21:9", cycle_count=16)
    f.draw()
    '''
from complex_fractals import *

class Mandelbrot(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
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

class Mandelbar(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 5

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.3775, 0.0)

        # Unique identifier for this fractal type
        identifier = 1

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="mandelbar"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="mandelbar_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class PerpendicularMandelbrot(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 4

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.3775, 0.0)

        # Unique identifier for this fractal type
        identifier = 2

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="perpendicular_mandelbrot"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="perpendicular_mandelbrot_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class CelticMandelbort(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 4

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.3775, 0.0)

        # Unique identifier for this fractal type
        identifier = 3

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="celtic_mandelbrot"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="celtic_mandelbrot_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class CelticMandelbar(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
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
        identifier = 4

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="celtic_mandelbar"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="celtic_mandelbar_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class PerpendicularCeltic(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 3

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.3775, 0.0)

        # Unique identifier for this fractal type
        identifier = 5

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="perpendicular_celtic"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="perpendicular_celtic_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class BurningShip(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 3

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.3775, 0.5)

        # Unique identifier for this fractal type
        identifier = 6

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="burning_ship"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="burning_ship_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class HeartMandelbrot(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 3

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.3775, 0.0)

        # Unique identifier for this fractal type
        identifier = 7

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="heart_mandelbrot"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="heart_mandelbrot_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class PerpendicularBurningShip(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 3

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.3775, 0.0)

        # Unique identifier for this fractal type
        identifier = 8

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="perpendicular_burning_ship"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="perpendicular_burning_ship_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class Buffalo(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 3

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.70, 0.5)

        # Unique identifier for this fractal type
        identifier = 9

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="buffalo"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="buffalo_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class HeartCeltic(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 2

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.5, 0.0)

        # Unique identifier for this fractal type
        identifier = 10

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="heart_celtic"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="heart_celtic_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)

class PerpendicularBuffalo(ComplexFractal):
    def __init__(self, width=1920, aspect_ratio="16:9", iter_max=750,
        oversample=3, real=-.3775, imag=0, zoom=1,
        rgb_phases=[0.0, 0.8, 0.15], random_phases=False, cycle_count=50,
        stripe_density=2, stripe_memory=.9, blend_factor=1.0, gpu=False):
        """Creates the mandelbrot set
        See ComplexFractal class for description of arguments
        """

        # The range of the imaginary axis. 
        # Used to determine range of real axes in super call
        im_range = 3

        # The 'center' point of the fractal
        # Used when creating images at non center point and zoom animations to ensure 
        # that images stay around center until zoom is deep enough to not
        center = complex(-0.5, 0.0)

        # Unique identifier for this fractal type
        identifier = 11

        # Call init of parent class, with all kwargs of this subclass' constructor
        loc = locals()
        loc.pop('self', None)
        loc.pop('__class__', None)
        super().__init__(**loc)

    def draw(self, filename="perpendicular_buffalo"):
        """Create a singular output image
        See _draw method of ComplexFractal class
        """
        self._draw(filename)
    
    def animate(self, start=1, end=2**30, rate=2, filename="perpendicular_buffalo_anim"):
        """Create a series of images that when played in order animate a zoom on the set
        See _animate method of ComplexFractal class
        """
        self._animate(start, end, rate, filename)
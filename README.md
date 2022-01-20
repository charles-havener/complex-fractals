<!-- Project Header -->
<br>
<p align="center">
  <h2 align="center">Complex Fractals</h2>
  <p align="center">
    Image generation of various fractals in the complex plane.
  </p>
</p>

<p align="center">Built with 
  <a href="https://www.python.org/downloads/release/python-378/">Python 3.7.8</a>, 
  <a href="https://numpy.org/">Numpy</a>, and
  <a href="https://numba.pydata.org/">Numba</a>.
</p>

<br>




<!--  Table of Contents -->
### Table of Contents
- [About the Project](#about-the-project)
- [Usage](#usage)
- [Parameters](#parameters)
  - [ComplexFractal](#complexfractal)
  - [Animate](#animate)
- [Examples](#examples)

<br>




<!--  List of todos -->
## Todo List
- Add additional fractals (3rd and 4th powers)?
- Have .animate() create an .mp4 or .gif rather than a series of images.

<br>




<!-- About section -->
# About The Project

- **todo - generic about segment**

<br>

## How it Works
Each fractal is generated using an iterative function. The mandelbrot, for example, uses the function &nbsp; <!-- $\color{#83a598}z_{n+1} = f(z_{n}) = z_n^{2}+c$ --> <img style="transform: translateY(0.2em) scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dz_%7Bn%2B1%7D%20%3D%20f(z_%7Bn%7D)%20%3D%20z_n%5E%7B2%7D%2Bc"> &nbsp; where &nbsp; <!-- $\color{#83a598}z_i$ --> <img style="transform: translateY(0.1em) scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dz_i"> &nbsp; and &nbsp; <!-- $\color{#83a598}c$ --> <img style="transform: translateY(0.0em) scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dc"> &nbsp; are both complex numbers in the form &nbsp; <!-- $\color{#83a598}a+bi$ --> <img style="transform: translateY(0.0em) scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Da%2Bbi"> &nbsp; with &nbsp; <!-- $\color{#83a598}i=\sqrt{-1}$ --> <img style="transform: translateY(0.3em) scale(1.1,1.1); background: nonoe;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Di%3D%5Csqrt%7B-1%7D"> &nbsp;. Here &nbsp; <!-- $\color{#83a598}c$ --> <img style="transform: translateY(0.0em)  scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dc"> &nbsp; is a constant representing the coordinate of a pixel and &nbsp; <!-- $\color{#83a598}z_0$ --> <img style="transform: translateY(0.1em)  scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dz_0"> &nbsp; is the point &nbsp; <!-- $\color{#83a598}(0,0)$ --> <img style="transform: translateY(0.3em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7D(0%2C0)"> &nbsp; in the complex plane. The point is iterated until it either escapes a given radius from the origin or the iteraiton count limit is hit. Points which do not escape are said to be part of the set (typically colored black), and points that do diverge are colored based on their highest iteration count before they escaped. The coloring is smoothed to give a nicer looking output.

<br>

# Usage

```sh
# After cloning the repository and navigating to the directory
$ python -m venv venv
$ .\venv\scripts\activate
$ pip install -r requirements.txt
```

```python
from complex_fractals import * # import all classes and functions
```

## Fractal Types
```python
ComplexFractal("list") # list all identifiers to console

""" output will look as follows. Either the number (as int) or name (as str) can be used as identifier parameter

-1 - list
 0 - mandelbrot
 1 - mandelbar
 .
 .
 .
11 - perpendicular_buffalo
"""
```
## Basic Usage
```python
f = ComplexFractal() # set up a mandelbrot with default parameters
f.draw() # create the image
```

<br>




<!-- Parameters -->
# Parameters

## ComplexFractal

```python
#rgb_phases used for all parameter images
phases = [0.4621369927925133,0.5109418659399724,0.5222266582635113]
```

### identifier
>see [Fractal Types](#fractal-types) for how to retrieve a list of possible identifiers. The integer and string are both valid inputs.


### width
>number of pixels in the horizontal dimension of the output image.


### aspect_ratio
>aspect ratio of the output image. Input as type str in the form "W:H". Defaults to "16:9" (1920x1080), another common aspect ration is "21:9" (3440x1440).
><p align="center">
  ><img src="Images\aspect_ratio_16-9.jpg" alt="16:9" title="16:9" width="200">
  ><img src="Images\aspect_ratio_21-9.jpg" alt="21:9" title="21:9" width="262.5">
></p>

```python
ComplexFractal(aspect_ratio="16:9", rgb_phases=phases, 
    filename="aspect_ratio_16-9").draw()
ComplexFractal(aspect_ratio="21:9", rgb_phases=phases,
    filename="aspect_ratio_21-9").draw()
```


### cycle_count
>the number of iterations before the colormap cycles back to the start. Smaller values yield >faster color transitions.
><p align="center">
  ><img src="Images\color_map.jpg" alt="color map" title="color map" width="600">
></p>
><p align="center">
  ><img src="Images\cycle_count_16.jpg" alt="cycle count 16" title="cycle count 16" width="200">
  ><img src="Images\cycle_count_32.jpg" alt="cycle count 32" title="cycle count 32" width="200">
  ><img src="Images\cycle_count_64.jpg" alt="cycle count 64" title="cycle count 64" width="200">
></p>

```python
ComplexFractal(cycle_count=16, rgb_phases=phases, 
    filename="cycle_count_16").draw()
ComplexFractal(cycle_count=32, rgb_phases=phases, 
    filename="cycle_count_32").draw()
ComplexFractal(cycle_count=64, rgb_phases=phases, 
    filename="cycle_count_64").draw()
```


### oversample
>scale the image dimensions by a factor of oversample. The image is then downscaled to the desired size by averaging oversample*oversample grids of pixels. Creates a cleaner image, but large oversample values can greatly increase computation times. Value must be greater than or equal to 1.
><p align="center">
  ><img src="Images\oversample_1.jpg" alt="oversample 1" title="oversample 1" width="500">
  ><img src="Images\oversample_4.jpg" alt="oversample 4" title="oversample 4" width="500">
></p>

```python
ComplexFractal(oversample=1, rgb_phases=phases, 
    filename="oversample_1").draw()
ComplexFractal(oversample=4, rgb_phases=phases, 
    filename="oversample_4").draw()
```

### real
>the real value to focus on or to zoom in on. Defaults to the center of the set.


### imag
>the imaginary value to focus on or to zoom in on. Defaults to the center of the set.


### zoom
>the depth of the zoom. Value should be greater than or equal to 1. Defaults to 1.


### rgb_phases
>phases used to create cyclic color map. Each value should be in the range [0.0, 1.0].
><p align="center">
  ><img src="Images\colormap_0.0-0.8-0.15.jpg" alt="colormap [0.0, 0.8, 0.15]" title="colormap [0.0, 0.8, 0.15]" width="250">
  ><img src="Images\colormap_0.05-0.21-0.31.jpg" alt="colormap [0.05, 0.21, 0.31]" title="colormap [0.05, 0.21, 0.31]" width="250">
  ><img src="Images\colormap_0.85-0.17-0.55.jpg" alt="colormap [0.85, 0.17, 0.55]" title="colormap [0.85, 0.17, 0.55]" width="250">
></p>

```python
# Can preview colormaps using custom values with...
ColorMap(rgb_phases=[0.0, 0.8, 0.15]).preview_colormap()

# Or preview random colormaps with...
ColorMap(random_phases=True).preview_colormap() # random values generated are output to console
```


### random_phases
>Whether random rgb phases should be used. Will always overide any values passed to rgb_phases if True. Defaults to False. 


### iter_max
>maximum number of iterations until a point that doesn't escape is considered part of the set. Deeper zoom levels require higher iter_max values.

<b>stripe_density</b>
>how dense the stripes are in the final image.
><p align="center">
  ><img src="Images\stripe_density_0.jpg" alt="stripe density 0" title="stripe density 0" width="200">
  ><img src="Images\stripe_density_2.jpg" alt="stripe density 2" title="stripe density 2" width="200">
  ><img src="Images\stripe_density_6.jpg" alt="stripe density 6" title="stripe density 6" width="200">
></p>

```python
ComplexFractal(stripe_density=0, rgb_phases=phases, 
    filename="stripe_density_0").draw()
ComplexFractal(stripe_density=2, rgb_phases=phases, 
    filename="stripe_density_2").draw()
ComplexFractal(stripe_density=6, rgb_phases=phases, 
    filename="stripe_density_6").draw()
```

<b>stripe_memory</b>
>the weight of historical values kept between iterations. Value should be in the range [0.0, 1.0]
><p align="center">
  ><img src="Images\stripe_memory_0.0.jpg" alt="stripe memory 0.0" title="stripe memory 0.0" width="200">
  ><img src="Images\stripe_memory_0.4.jpg" alt="stripe memory 0.4" title="stripe memory 0.4" width="200">
  ><img src="Images\stripe_memory_0.9.jpg" alt="stripe memory 0.9" title="stripe memory 0.9" width="200">
></p>

```python
ComplexFractal(stripe_memory=0.0, rgb_phases=phases, 
    filename="stripe_memory_0.0").draw()
ComplexFractal(stripe_memory=0.4, rgb_phases=phases, 
    filename="stripe_memory_0.4").draw()
ComplexFractal(stripe_memory=0.9, rgb_phases=phases, 
    filename="stripe_memory_0.9").draw()
```


<b>blend_factor</b>
>how strong of a showing the stripes make in the final image, value in [0.1, 1.0].
><p align="center">
  ><img src="Images\blend_factor_0.33.jpg" alt="blend factor 0.33" title="blend factor 0.33" width="200">
  ><img src="Images\blend_factor_0.66.jpg" alt="blend factor 0.66" title="blend factor 0.66" width="200">
  ><img src="Images\blend_factor_1.0.jpg" alt="blend factor 1.00" title="blend factor 1.0" width="200">
></p>

```python
ComplexFractal(blend_factor=0.33, rgb_phases=phases, 
    filename="blend_factor_0.33").draw()
ComplexFractal(blend_factor=0.66, rgb_phases=phases, 
    filename="blend_factor_0.66").draw()
ComplexFractal(blend_factor=1.0, rgb_phases=phases, 
    filename="blend_factor_1.0").draw()
```


<b>gpu</b>
>Compute with GPU or with CPU. True will render using the GPU. Defaults to False. GPU will render the image significantly faster than CPU but requires the CUDA toolkit to be installed. Details on how to install it to work with Numba can be found [here](http://numba.pydata.org/numba-doc/latest/cuda/overview.html#setting-cuda-installation-path).


<b>filename</b>
>The name to be assigned to the output image. Defaults to the stringed version of the identifier.


## Animate

<b>start</b>
>the initial zoom level. Should be greater than or equal to 1.


<b>end</b>
>the target zoom level to be reached in the final frame. Must be greater than start value.


<b>rate</b>
>the speed at which the zoom level approaches the end value. Must be strictly greater than 1.

<br>




<!-- Examples -->
# Examples
- **todo create example images/gifs/mp4s**
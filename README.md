<!-- Project Header -->
<br>
<p align="center">
  <h2 align="center">Complex Fractals</h2>
  <p align="center">
    Image generation of various fractals in the complex plane.
    <!-- TODO: create some high rez images/gifs for an imgur gallery?
    <br />
    <a href="https://imgur.com/gallery/jqMogwz"><strong>4000x4000 Example Output Images »</strong></a>
    <br />
    TODO end -->
  </p>
</p>

<p align="center">Built with 
  <a href="https://www.python.org/downloads/release/python-378/">Python 3.7.8</a>, 
  <a href="https://numpy.org/">Numpy</a>, and
  <a href="https://numba.pydata.org/">Numba</a>, 
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

**todo - generic about segment**

<br>

## How it Works
Each fractal is generated using an iterative function. The mandelbrot, for example, uses the function &nbsp; <!-- $\color{#83a598}f(z_{n+1}) = z_n^{2}+c$ --> <img style="transform: translateY(0.2em) scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Df(z_%7Bn%2B1%7D)%20%3D%20z_n%5E%7B2%7D%2Bc"> &nbsp; where &nbsp; <!-- $\color{#83a598}z_i$ --> <img style="transform: translateY(0.1em) scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dz_i"> &nbsp; and &nbsp; <!-- $\color{#83a598}c$ --> <img style="transform: translateY(0.0em) scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dc"> &nbsp; are both complex numbers in the form &nbsp; <!-- $\color{#83a598}a+bi$ --> <img style="transform: translateY(0.0em) scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Da%2Bbi"> &nbsp; with &nbsp; <!-- $\color{#83a598}i=\sqrt{-1}$ --> <img style="transform: translateY(0.3em) scale(1.1,1.1); background: nonoe;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Di%3D%5Csqrt%7B-1%7D"> &nbsp;. Here &nbsp; <!-- $\color{#83a598}c$ --> <img style="transform: translateY(0.0em)  scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dc"> &nbsp; is a constant representing the coordinate of a pixel and &nbsp; <!-- $\color{#83a598}z_0$ --> <img style="transform: translateY(0.1em)  scale(1.1,1.1); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dz_0"> &nbsp; is the point &nbsp; <!-- $\color{#83a598}(0,0)$ --> <img style="transform: translateY(0.3em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7D(0%2C0)"> &nbsp; in the complex plane. The point is iterated until it either escapes a given radius from the origin or the iteraiton count limit is hit. Points which do not escape are said to be part of the set (typically colored black), and points that do diverge are colored based on their highest iteration count before they escaped. The coloring is smoothed to give a nicer looking output.

<br>

# Usage

```sh
# After cloning the repository onto your local machine and navigating to the directory
$ python -m venv venv
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
**todo - explanations and accompanying images where necessary**
## ComplexFractal
identifier=0
width=480
aspect_ratio="16:9"
cycle_count=16
oversample=2 
real=-0.3775
imag=0.0
zoom=1
rgb_phases=[0.0, 0.8, 0.15]
random_phases=True 
iter_max=350
stripe_density=2
stripe_memory=0.9
blend_factor=1.0
gpu=False
filename=None

## Animate
start=1
end=2**10
rate=2

<br>




<!-- Examples -->
# Examples
**todo**
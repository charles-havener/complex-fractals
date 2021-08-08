<!-- Project Header -->

<br />
<p align="center">

  <h3 align="center">Complex Fractals</h3>

  <p align="center">
    Image generation of various fractals in the complex plane.
    <!-- TODO: create some high rez images/gifs for an imgur gallery?
    <br />
    <a href="https://imgur.com/gallery/jqMogwz"><strong>4000x4000 Example Output Images »</strong></a>
    <br />
    TODO end -->
  </p>
</p>

<p align="center">
  <img src="Images\OutputExamples.png" alt="Line Examples" width="500">
</p>

<p align="center">Built with 
  <a href="https://www.python.org/downloads/release/python-378/">Python 3.7.8</a>, 
  <a href="https://numpy.org/">Numpy</a>, and
  <a href="https://pillow.readthedocs.io/en/stable/">Pillow</a>, 
</p>

<br>

### Todo List
- <del>Add additional fractals</del>
- <del>Add color map options</del>
- Add zooming options to create zoom animations (deeper zooms will require use of Decimal or some other high precision library)
- GPU rendering option
- <del>Create SVG images for LaTeX formulas since github doesn't render them</del>

<br>

# About The Project

## How it Works

### General Complex Fractals
Each fractal is generated using a recursive function. The mandelbrot, for example, uses the function <!-- $\color{#83a598}f_{c}(z) = z^{2}+c$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Df_%7Bc%7D(z)%20%3D%20z%5E%7B2%7D%2Bc"> where <!-- $\color{#83a598}f_i$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Df_i"> and <!-- $\color{#83a598}c$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dc"> are imaginary numbers in the form <!-- $\color{#83a598}a+bi$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Da%2Bbi"> with <!-- $\color{#83a598}i$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Di"> being the <!-- $\color{#83a598}\sqrt{-1}$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7D%5Csqrt%7B-1%7D">. Here <!-- $\color{#83a598}c$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dc"> is a constant representing the <!-- $\color{#83a598}(Re, Im)$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7D(Re%2C%20Im)"> coordinate of a pixel and <!-- $\color{#83a598}z_0$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dz_0"> is the point <!-- $\color{#83a598}(0,0)$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7D(0%2C0)"> on the complex plane. The point is iterated until it either escapes a given radius or the iteraiton count limit is hit. Points which do not escape are said to be part of the set (typically colored black), and points that do diverge are colored based on their highest iteration count before they escaped. The coloring is smoothed to give a nicer looking output.

### Julia Sets
Generated the same way as general complex fractals, however <!-- $\color{#83a598}z_0$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dz_0"> is initialized to the <!-- $\color{#83a598}(Re, Im)$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7D(Re%2C%20Im)"> coordinate of the pixel and <!-- $\color{#83a598}c$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Dc"> is a constant in the form <!-- $\color{#83a598}a+bi$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7Da%2Bbi"> such as <!-- $\color{#83a598}-0.7269+0.1889i$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7D-0.7269%2B0.1889i"> or <!-- $\color{#83a598}-0.4+0.6i$ --> <img style="transform: translateY(0.1em); background: none;" src="https://render.githubusercontent.com/render/math?math=%5Ccolor%7B%2383a598%7D-0.4%2B0.6i">. The Julia set class here is for the Mandelbrot set, although they do exist for all of the general complex fractals.

<br>


<!-- PARAMS
    aspect_ratio: either "16:9" or "21:9" anything else will be a square image that may look warped
    xdim: width of the image (height calculated off of aspect ratio)
    coords: [min_x, max_x, min_y, max_y]
    filename: name of output file
    color_map: option via showColormaps()
    max_iterations: max iteration to hit for point to be considered in set
    escape_radius: points who iterate to value outside of this value are considered out of set

    julia has additional parameters:
    real, imag: (Re, Im) point on the complex plane to generate for
-->


## Fractal Types and Color Maps
<br>

```python
from complex_fractals import * # import all classes and functions

showClasses() # list class names of fractal types in console
showColormaps() # list color map options in console
```

<p align="left">
  <img src="Images\FractalTypes.png" alt="Line Examples" width="1000">
</p>

<br>

<p align="left">
  <img src="Images\ColorOptions.png" alt="Line Examples" width="1250">
</p>

<br>
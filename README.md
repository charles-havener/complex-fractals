<!-- Project Header -->

<br />
<p align="center">

  <h3 align="center">Complex Fractals</h3>

  <p align="center">
    Image generation of various fractals in the complex plane.
    <!-- TODO: create some high rez images for an imgur gallery?
    <br />
    <a href="https://imgur.com/gallery/jqMogwz"><strong>4000x4000 Example Output Images »</strong></a>
    <br />
    TODO end -->
  </p>
</p>

<p align="center">
  <img src="Images\OutputExamples.png" alt="Line Examples" width="500">
  <!--TODO create collage of example images -->
</p>

<p align="center">Built with 
<a href="https://www.python.org/downloads/release/python-378/">Python 3.7.8</a>, 
<a href="https://numpy.org/">Numpy</a>, and
<a href="https://pillow.readthedocs.io/en/stable/">Pillow</a>, 
</p>

<br>


<!-- About the Project -->

# About The Project

### Todo List
- Add zooming options to create zoom animations (will require use of Decimal for high precision with deeper zooms)
- Multithreading (to speed up point divergence calculations)
- GUI or Flask site to replace editing main.py to create images

<br>

## How it Works

### General Complex Fractals
Each fractal is generated using a recursive function. The mandelbrot, for example, uses the function $f_{n+1}(z) = f_{n}^{2}+c$ where  $f_i$ and $c$ are imaginary numbers in the form $a+bi$ with $i$ being the $\sqrt{-1}$. Here $c$ is a constant representing the $(Re, Im)$ coordinate of a pixel and $z_0$ is the point $(0,0)$ on the complex plane. The point is iterated until it either escapes a given radius or the iteraiton count limit is hit. Points which do not escape are said to be part of the set (typically colored black), and points that do diverge are colored based on their highest iteration count before they escaped. The coloring is smoothed to give a nicer looking output.

### Julia Sets
Generated the same way as general complex fractals, however $z_0$ is initialized to the $(Re, Im)$ coordinate of the pixel and $c$ is a constant in the form $a+bi$ such as $-0.7269+0.1889i$ or $-0.4+0.6i$. The Julia set class here is for the Mandelbrot set, although they do exist for all of the general complex fractals.

<br>



<!-- Fractal Types and Color Maps -->

## Fractal Types and Color Maps
<br>

<p align="left">
  <img src="Images\FractalTypes.png" alt="Line Examples" width="1000">
  <!--TODO create collage of example images -->
</p>

<br>

<p align="left">
  <img src="Images\ColorOptions.png" alt="Line Examples" width="1250">
  <!--TODO create collage of example images -->
</p>

<br>
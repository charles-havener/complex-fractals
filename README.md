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
- <del>Add additional fractals</del>
- <del>Add color map options</del>
- Add zooming options to create zoom animations (will require use of Decimal for high precision with deeper zooms)
- Multithreading (to speed up point divergence calculations)
- GUI or Flask site to replace editing main.py to create images
- Create SVG images for LaTeX formulas since github doesn't render them

<br>

## How it Works

### General Complex Fractals
Each fractal is generated using a recursive function. The mandelbrot, for example, uses the function <!-- $f_{n+1}(z) = f_{n}^{2}+c$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=f_%7Bn%2B1%7D(z)%20%3D%20f_%7Bn%7D%5E%7B2%7D%2Bc"> where <!-- $f_i$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=f_i"> and <!-- $c$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=c"> are imaginary numbers in the form <!-- $a+bi$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=a%2Bbi"> with <!-- $i$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=i"> being the <!-- $\sqrt{-1}$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=%5Csqrt%7B-1%7D">. Here <!-- $c$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=c"> is a constant representing the <!-- $(Re, Im)$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=(Re%2C%20Im)"> coordinate of a pixel and <!-- $z_0$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=z_0"> is the point <!-- $(0,0)$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=(0%2C0)"> on the complex plane. The point is iterated until it either escapes a given radius or the iteraiton count limit is hit. Points which do not escape are said to be part of the set (typically colored black), and points that do diverge are colored based on their highest iteration count before they escaped. The coloring is smoothed to give a nicer looking output.

### Julia Sets
Generated the same way as general complex fractals, however <!-- $z_0$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=z_0"> is initialized to the <!-- $(Re, Im)$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=(Re%2C%20Im)"> coordinate of the pixel and <!-- $c$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=c"> is a constant in the form <!-- $a+bi$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=a%2Bbi"> such as <!-- $-0.7269+0.1889i$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=-0.7269%2B0.1889i"> or <!-- $-0.4+0.6i$ --> <img style="transform: translateY(0.1em); background: rgba(131,165,152,1);" src="https://render.githubusercontent.com/render/math?math=-0.4%2B0.6i">. The Julia set class here is for the Mandelbrot set, although they do exist for all of the general complex fractals.

<br>


## Fractal Types and Color Maps
<br>

<p align="left">
  <img src="Images\FractalTypes.png" alt="Line Examples" width="1000">
</p>

<br>

<p align="left">
  <img src="Images\ColorOptions.png" alt="Line Examples" width="1250">
</p>

<br>
from PIL import Image
import numpy as np

# smooth coloring
def color(z, i, R=4):
    if abs(z) < R:
        return 0, 0, 0
    v = np.log2(i + R - np.log2(np.log2(abs(z)))) / 5
    if v < 1.0:
        return v**4, v**1, v**1.5 # outer
    else:
        v = max(0, 2 - v)
        return v**2.2, v**1, v**1.5 # inner

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

def burningShip(R=4):
    z = np.zeros((dimen_y, dimen_x), dtype=np.complex)
    X = np.linspace(-3.0, 2.33, dimen_x).reshape((1, dimen_x))
    Y = np.linspace(-2.0,1.0,dimen_y).reshape((dimen_y, 1))
    c = X+1j*Y

    img_data = np.zeros((dimen_y, dimen_x), dtype=np.float32)
    is_not_diverged = np.ones((dimen_y, dimen_x), dtype=np.float32)

    print(f"  -iterating points")
    for _ in range(iterations):
        z = np.where(is_not_diverged, (abs(z.real)+abs(z.imag)*1j)**2 + c, z)
        is_not_diverged = (np.abs(z)<4).astype(np.float32) # 0->diverged; 1->not
        # increment iteration of non diverged points
        img_data += is_not_diverged

    # get pixel colors
    print(f"  -generating colors")
    r,g,b = np.frompyfunc(color, 3, 3)(z, img_data, R)
    img_c = np.dstack((r,g,b))

    print(f"  -writing image")
    return np.uint8(img_c * 255)


def mandelbrot(R=4):
    z = np.zeros((dimen_y, dimen_x), dtype=np.complex)
    X = np.linspace(-3.33, 2.0, dimen_x).reshape((1, dimen_x))
    Y = np.linspace(-1.5,1.5,dimen_y).reshape((dimen_y, 1))
    c = X+1j*Y

    img_data = np.zeros((dimen_y, dimen_x), dtype=np.float32)
    is_not_diverged = np.ones((dimen_y, dimen_x), dtype=np.float32)

    print(f"  -iterating points")
    for _ in range(iterations):
        z = np.where(is_not_diverged, z**2 + c, z)
        is_not_diverged = (np.abs(z)<4).astype(np.float32) # 0->diverged; 1->not
        # increment iteration of non diverged points
        img_data += is_not_diverged

    # get pixel colors
    print(f"  -generating colors")
    r,g,b = np.frompyfunc(color, 3, 3)(z, img_data, R)
    img_c = np.dstack((r,g,b))

    print(f"  -writing image")
    return np.uint8(img_c * 255)


def julia(c, R=4):
    c = np.full((dimen_y, dimen_x), c,dtype=np.complex)
    X = np.linspace(-2.67, 2.67, dimen_x).reshape((1, dimen_x))
    Y = np.linspace(-1.5,1.5,dimen_y).reshape((dimen_y, 1))
    z = X+1j*Y

    img_data = np.zeros((dimen_y, dimen_x), dtype=np.float32)
    is_not_diverged = np.ones((dimen_y, dimen_x), dtype=np.float32)

    print(f"  -iterating points")
    for _ in range(iterations):
        z = np.where(is_not_diverged, z**2 + c, z)
        is_not_diverged = (np.abs(z)<4).astype(np.float32) # 0->diverged; 1->not
        # increment iteration of non diverged points
        img_data += is_not_diverged

    # get pixel colors
    print(f"  -generating colors")
    r,g,b = np.frompyfunc(color, 3, 3)(z, img_data, R)
    img_c = np.dstack((r,g,b))

    print(f"  -writing image")
    return np.uint8(img_c * 255)


if __name__ == "__main__":
    dimen_x, dimen_y = 960, 540
    iterations = 255
    R = 4

    display = Image.fromarray(mandelbrot(), 'RGB')
    display.save('mandelbrot.bmp')

    display = Image.fromarray(burningShip(), 'RGB')
    display.save('burning.bmp')

    c = -0.7269+0.1889j
    display = Image.fromarray(julia(c), 'RGB')
    display.save('julia1.bmp')

    c = -0.835-0.2321j
    display = Image.fromarray(julia(c), 'RGB')
    display.save('julia2.bmp')

    c = 0.285+0.01j
    display = Image.fromarray(julia(c), 'RGB')
    display.save('julia3.bmp')

    c = -0.8+0.156j
    display = Image.fromarray(julia(c), 'RGB')
    display.save('julia4.bmp')
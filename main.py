from PIL import Image
import numpy as np

# smooth coloring
def color(z, i, R=4):
    if abs(z) < R:
        return 0, 0, 0
    v = np.log2(i + R - np.log2(np.log2(abs(z)))) / 5
    if v < 1.0:
        return v**4, v**2.5, v
    else:
        v = max(0, 2 - v)
        return v, v**1.5, v**3

def burningShip(R=4):
    z = np.zeros((dimen_y, dimen_x), dtype=np.complex)
    X = np.linspace(-2.67, 2.67, dimen_x).reshape((1, dimen_x))
    Y = np.linspace(-1.5,1.5,dimen_y).reshape((dimen_y, 1))
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
    X = np.linspace(-2.67, 2.67, dimen_x).reshape((1, dimen_x))
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

    c = -0.7269+0.1889j
    R = 4

    #display = Image.fromarray(mandelbrot(), 'RGB')
    #display = Image.fromarray(julia(c), 'RGB')
    display = Image.fromarray(burningShip(), 'RGB')
    display.save('out.bmp')
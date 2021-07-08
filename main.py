from decimal import Decimal, getcontext

class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]

class Dec:
    def __init__(self, val):
        if type(val)!=str:
            val = str(val)
        self.val = Decimal(val)

class ComplexNumber:
    def __init__(self, real, img):
        self.real = Dec(real).val
        self.img = Dec(img).val
    
    def __repr__(self):
        if self.img >= 0:
            return f"{self.real}+{self.img}i"
        return f"{self.real}{self.img}i"

    def __add__(self, o):
        return ComplexNumber(self.real + o.real, self.img + o.img)

    def __sub__(self, o):
        return ComplexNumber(self.real - o.real, self.img - o.img)

    def __truediv__(self, o):
        o = Dec(o).val
        return ComplexNumber(self.real/o, self.img/o)

    def __mul__(self, o):
        real = self.real*o.real - self.img*o.img
        img = self.real*o.img + self.img*o.real
        return ComplexNumber(real, img)


class ComplexImg:
    def __init__(self, width=1980, height=1080, debug=False):
        self.debug = debug

        # Initializes evenly around 0+0i
        self.width = width
        self.height = height
        self.__setInitialCorners(self.width, self.height)

        self.zoom_rate = Dec('1.001').val
        self.destination = ComplexNumber(-1,2) #! need real value at some point

        if self.debug:
            print(f"\nDEBUG MODE: ENABLED\n")
            print(f"Width: {self.width}")
            print(f"Height: {self.height}")
            print(f"Zoom Rate: {self.zoom_rate}")
            print(f"Destination: {self.destination}")
            print(f"Initial Corners:\n\tTop Left: {self.top_left}\n\tTop Right: {self.top_right}\n\tBottom Left: {self.bottom_left}\n\tBottom Right: {self.bottom_right}\n")

    # TODO: get starting real/img range for set
    def __setInitialCorners(self, width, height):
        self.top_left = ComplexNumber(-Decimal(height/2), Decimal(width/2))
        self.top_right = ComplexNumber(Decimal(height/2), Decimal(width/2))
        self.bottom_left = ComplexNumber(-Decimal(height/2), -Decimal(width/2))
        self.bottom_right = ComplexNumber(Decimal(height/2), -Decimal(width/2))

    def setWidth(self, width):
        self.width = width
        if self.debug:
            print(f"Updated width: {self.width}\n")

    def setHeight(self, height):
        self.height = height
        if self.debug:
            print(f"Updated height: {self.height}\n")

    def setDims(self, width, height):
        self.setWidth(width)
        self.setHeight(height)

    def setZoomRate(self, z):
        self.zoom_rate = Dec(z).val
        if self.debug:
            print(f"Updated zoom rate: {self.zoom_rate}\n")

    def setDestination(self, r, i):
        self.destination = ComplexNumber(r, i)
        if self.debug:
            print(f"Updated destination: {self.destination}\n")

    def run(self, iterations=1):
        total = iterations
        while iterations>0:
            if self.debug:
                print(f"Running iteration {total-iterations+1} of {total}: {((total-iterations)/total)*100:.2f}%")

            vals = self.__generateValues() # TODO: actual formula in function instead of temp
            print(vals)
            #TODO: histogram equalization of values?? or just assign colors based on vals [0, max)
            #TODO: create image
            self.__setNextIterationCorners()
            iterations-=1
            print("\n")

    def __setNextIterationCorners(self):
        # Sets edge corners of next iteration. Attempts to center on destination, but will not go beyond 
        # original bounds allowing for a smooth zoom transition towards  destination points nearer to edges
        next_real_range = (self.top_right.real - self.top_left.real)/self.zoom_rate
        next_img_range = (self.top_right.img - self.bottom_right.img)/self.zoom_rate

        # Update coords of top right and set the others based on those values
        self.top_right.real = min(self.top_right.real, self.destination.real+(next_real_range/2))
        self.top_right.img = min(self.top_right.img, self.destination.img+(next_img_range/2))

        self.top_left = ComplexNumber(self.top_right.real-next_real_range, self.top_right.img)
        self.bottom_right = ComplexNumber(self.top_right.real, self.top_right.img-next_img_range)
        self.bottom_left = ComplexNumber(self.top_right.real - next_real_range, self.top_right.img - next_img_range)

        if self.debug:
            print("Next edge corners:")
            print(f"\t{self.top_left}  {self.top_right}")
            print(f"\t{self.bottom_left}  {self.bottom_right}")

    def __generateValues(self):
        real_step_size = (self.top_right.real-self.top_left.real)/self.width
        img_step_size = (self.top_right.img-self.bottom_right.img)/self.height
        reals = [self.top_left.real+(real_step_size*w)+real_step_size/2 for w in range(self.width)]
        imgs = [self.bottom_right.img+(img_step_size*h)+img_step_size/2 for h in range(self.height)]

        vals = [[-1]*self.height for _ in range(self.width)]
        for r in range(len(reals)):
            for i in range(len(imgs)):
                vals[r][i] = self.__mandelbrot(ComplexNumber(reals[r], imgs[i]))
        return vals

    def __mandelbrot(self, c):
        iteration = 0
        z = ComplexNumber(0,0)
        while iteration < max_iterations:
            if z.real*z.real + z.img*z.img > 4:
                return iteration/max_iterations
            z = z*z+c
            iteration+=1
        return 1

def setPrecision(precision):
    getcontext().prec = precision

def main():
    setPrecision(precision)
    img = ComplexImg(6,6,debug=True)
    img.setZoomRate(2)
    img.setDestination(0,0)
    img.setDims(10,10)
    img.run(1)

if __name__ == "__main__":
    precision = 100
    max_iterations = 200
    l = timeit(main, number=1)
    print("runtime:", l, "seconds")
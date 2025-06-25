from math import sqrt, atan

def clamp(x : float, m : float, M : float) -> float:
    if x < m:
        return m
    if x > M:
        return M
    return x

def dot(a : tuple, b : tuple) -> float:
    return a[0] * b[0] + a[1] * b[1] 

def length(x : tuple) -> float:
    return sqrt(dot(x, x))

def d2(X : tuple, stroke : list, sqrtA : float) -> float:
    integral = 0.
    for i in range(1, len(stroke)):
        x0 = stroke[i-1]
        d0 = (x0[0] - X[0], x0[1] - X[1])
        dir = (stroke[i][0] - x0[0], stroke[i][1] - x0[1])
        dist = length(dir)
        x1 = (dir[0]/dist, dir[1]/dist)
        # norm2(d0 + t*x1) = np.dot(d0 + t*x1, d0 + t*x1)
        c = dot(d0, d0)
        b = dot(x1, d0) * 2
        a = dot(x1, x1)
        u = b / (2*a)
        v = c - a*u*u # (4*a*c - b*b)/(4*a)
        if v <= 1e-4:
            # v = 0: dir == +-d0, X is colinear with the edge
            if -dist-1e-4 <= u <= 1e-4: # X is inside the edge
                return 0.
            else: # X is outside the edge
                primitive = lambda t: -1./(a*(t+u))
        else:
            invsqrtav = 1./sqrt(a*v)
            primitive = lambda t: atan((t+u)*invsqrtav*a)*invsqrtav
        integral += primitive(dist) - primitive(0)
    return sqrtA * integral**(-1./2)

def d2grad(x : tuple, stroke : list, sqrtA : float) -> tuple:
    dx = 5.0
    d2here : float = d2(x, stroke, sqrtA)
    right : tuple = (x[0] + dx, x[1])
    down : tuple = (x[0], x[1] + dx)
    res : tuple = ((d2(right, stroke, sqrtA) - d2here) / dx, (d2(down, stroke, sqrtA) - d2here) / dx)
    return res

# À appeler une fois au début de l'algo, puis utiliser son résultat en dernier argument de d2grad
def getSqrtA(stroke : list) -> float:
    return sqrt(sum([length((stroke[i][0] - stroke[i - 1][0], stroke[i][1] - stroke[i - 1][1])) for i in range(1, len(stroke))]))

def optimizeOneRib(ribs : list, threshold : float, lengths : list, i : int):
    (beg_x, beg_y), (end_x, end_y) = ribs[i]

    if i <= 0: lmin = lengths[1]
    elif i >= len(ribs) - 1: lmin = lengths[len(ribs) - 2]
    else: lmin = min(lengths[i - 1], lengths[i + 1])
    
    if lengths[i] > threshold * lmin:
        if i == 0: lmoy = lengths[1]
        elif i == len(ribs) - 1: lmoy = lengths[len(ribs) - 2]
        else: lmoy = (lengths[i + 1] + lengths[i - 1]) / 2

        unitDiff = ((end_x - beg_x) / lengths[i], (end_y - beg_y) / lengths[i])
        ribs[i] = (ribs[i][0], (beg_x + lmoy * unitDiff[0], beg_y + lmoy * unitDiff[1]))

def optimizeRibs(ribs : list, threshold : float = 1.25, nbIterations : int = 3):
    lengths = [length((end_x - beg_x, end_y - beg_y)) for ((beg_x, beg_y), (end_x, end_y)) in ribs]
    
    for _ in range(nbIterations):
        # odd ribs
        for i in range(1, len(ribs) - 1, 2):
            optimizeOneRib(ribs, threshold, lengths, i)

        # even ribs
        for i in range(2, len(ribs) - 1, 2):
            optimizeOneRib(ribs, threshold, lengths, i)

        # first rib
        optimizeOneRib(ribs, threshold, lengths, 0)

        # last rib
        optimizeOneRib(ribs, threshold, lengths, len(ribs) - 1)
            
# optimizeRibs([((1, 2), (2, 3)), ((1, 2), (2, 3)), ((8, 2), (2, 10)), ((1, 2), (2, 3)), ((1, 2), (2, 3))])

from math import sin, cos
from PIL import Image

def testd2():
    stroke = [(400 + 300 * cos(theta * 3.14159 / 180), 400 + 300 * sin(theta * 3.14159 / 180)) for theta in range(0, 300, 20)]
    # stroke = [(x, 400) for x in range(200, 600, 50)]
    img = Image.new(mode="RGB", size=(800, 800))
    pixels = img.load()

    sqrtA = getSqrtA(stroke)

    for y in range(800):
        for x in range(800):
            pixels[x, y] = (int(255 * abs(sin(0.2 * d2((x, y), stroke, sqrtA)))), 0, 0)

    img.show()

testd2()
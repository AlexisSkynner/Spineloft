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

def mix(a : float, b : float, t : float) -> float:
    return a * (1.0 - t) + b * t

def sdfSegment(p : tuple, a : tuple, b : tuple) -> float:
    ba = b[0] - a[0], b[1] - a[1]
    pa = p[0] - a[0], p[1] - a[1]
    h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0)
    return length((pa[0] - ba[0] * h, pa[1] - ba[1] * h))

def smin(a : float, b : float, k : float) -> float:
    h = clamp(0.5 + 0.5 * (a - b) / k, 0.0, 1.0)
    return mix(a, b, h) - k * h * (1.0 - h)

def oldd2(x : tuple, stroke : list) -> float:
    k = 10.0
    locMin = 9876543210.0
    for p_i in range(len(stroke) - 1):
        d = sdfSegment(x, stroke[p_i], stroke[p_i + 1])
        locMin = smin(locMin, d, k)
    return locMin

def I(x : tuple, T : float, A : tuple, B : tuple) -> float:
    l = length((B[0] - A[0], B[1] - A[1]))
    (x0, y0) = (x[0] - A[0], x[1] - A[1])
    (x1, y1) = ((B[0] - A[0]) / l, (B[1] - A[1]) / l)
    a = 1
    b = -2 * (x0 * x1 + y0 * y1)
    c = x0 * x0 + x1 * x1
    d = b / (2 * a)
    e2 = c / a - d * d
    if e2 <= 1e-4:
        if -l-1e-4 <= d <= 1e-4: # X is inside the edge
            return 0.
        return 1 / d - 1 / (T + d)
    else:
        e = sqrt(e2)
        return 1 / e * (atan((T + d) / e) - atan(d / e))

def segd2(x : tuple, A : tuple, B : tuple) -> float:
    T = length((B[0] - A[0], B[1] - A[1]))
    return I(x, T, A, B) - I(x, 0, A, B)

def newd2(x : tuple, stroke : list) -> float:
    A = sum([length((stroke[i + 1][0] - stroke[i][0], stroke[i + 1][1]-stroke[i][1])) for i in range(len(stroke) - 1)])
    totI = sum([segd2(x, stroke[i], stroke[i + 1]) for i in range(len(stroke) - 1)])
    return sqrt(A) / sqrt(totI)


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
    # l : float = length(res)
    # return (res[0] / l, res[1] / l)

def getSqrtA(stroke : list) -> float:
    return sqrt(sum([length((stroke[i][0] - stroke[i - 1][0], stroke[i][1] - stroke[i - 1][1])) for i in range(1, len(stroke))]))

# from math import sin, cos
# from PIL import Image

# def testd2():
#     stroke = [(400 + 300 * cos(theta * 3.14159 / 180), 400 + 300 * sin(theta * 3.14159 / 180)) for theta in range(0, 300, 20)]
#     # stroke = [(x, 400) for x in range(200, 600, 50)]
#     img = Image.new(mode="RGB", size=(800, 800))
#     pixels = img.load()

#     sqrtA = getSqrtA(stroke)

#     for y in range(800):
#         for x in range(800):
#             pixels[x, y] = (int(255 * abs(sin(0.2 * d2((x, y), stroke, sqrtA)))), 0, 0)

#     img.show()

# testd2()
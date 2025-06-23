from math import sqrt

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

def d2(x : tuple, stroke : list) -> float:
    k = 32.0
    locMin = 9876543210.0
    for p_i in range(len(stroke) - 1):
        d = sdfSegment(x, stroke[p_i], stroke[p_i + 1])
        locMin = smin(locMin, d, k)
    return locMin

def d2grad(x : tuple, stroke : list) -> tuple:
    dx = 5.0
    here = d2(x, stroke)
    res = (d2((x[0] + dx, x[1]), stroke) - here) / dx, (d2((x[0], x[1] + dx), stroke) - here) / dx
    return res / length(res)

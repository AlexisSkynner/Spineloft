import math
from . import d2 

def distance(x,y):
    return (x[0]-y[0])**2 +  (x[1]-y[1])**2

def generate_points(p1 : tuple, p2 : tuple , nb_points : int, d : int, stroke : list):

    total_length = math.sqrt(distance(p2, p1))

    direction = ((p2[0] - p1[0]) / total_length, (p2[1] - p1[1]) / total_length)

    for i in range(nb_points):
        stroke.append((p1[0] + direction[0] * d * (i + 1), p1[1] + direction[1] * d * (i + 1)))

def point_in_poly(x: int, y: int, poly: list[tuple]) -> bool:
    """
    Teste si un point (x, y) est dans un polygone `poly` (liste de points fermée)
    """
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
            inside = not inside
        j = i
    return inside

def contour_detection(width : int, height : int, pixels : list, ignore_zones: list[list[tuple]]): 

    threshold = 30
    edges = [0] * width * height

    # Détection simple : différence entre pixels voisins
    for y in range(1, height - 1):
        for x in range(1, width - 1):

            # Vérifie si (x, y) est dans une des zones à ignorer
            ignore = any(point_in_poly(x, y, zone) for zone in ignore_zones)
            if ignore:
                continue

            # Gradient approximatif (Sobel simplifié)
            gx = abs(pixels[y*width+x+1] - pixels[y*width+x-1])
            gy = abs(pixels[(y+1)*width+x] - pixels[(y-1)*width+x])
            gradient = gx + gy

            # Seuil de détection des bords réglables 
            edges[x + y * width] = 255 if gradient > threshold else 0
    return edges

def intersect(width : int, height : int, img : list, stroke : list, ignore_zones: list[list[tuple]], type : int) -> list:
    pixels = contour_detection(width, height, img, ignore_zones) 

    SqrtA = d2.getSqrtA(stroke)
    ribs = []
    alpha = 2.0
    correction = 10.0
    dmax = 10 

    if type == 0 : 
        stroke_arranged = []
        for i in range(0, len(stroke) - 1):
            if i !=0:
                stroke_arranged.append(stroke[i])

            d = distance(stroke[i], stroke[i+1])
            nb_points = 0 

            while d >dmax :
                nb_points += 1
                d /= 2
            
            generate_points(stroke[i],stroke[i+1],nb_points, d, stroke_arranged, )
        stroke_arranged.append(stroke[len(stroke)-1])
    else :
        stroke_arranged = stroke

    for i in range(1, len(stroke_arranged) - 1):

        #Init of the two first points close to stroke point for determining the left and right point of the rib
        p1 = stroke_arranged[i]
        p2 = stroke_arranged[i + 1]
        middle = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)

        dx = p2[0] - middle[0]
        dy = middle[1] - p2[1]

        # Right
        rx = dx * math.cos(math.pi/2) + dy * math.sin(math.pi/2)
        ry = dx * math.sin(math.pi/2) - dy * math.cos(math.pi/2)
        right_ext = (rx * correction + middle[0], ry * correction + middle[1])

        # Left
        lx = dx * math.cos(-math.pi/2) + dy * math.sin(-math.pi/2)
        ly = dx * math.sin(-math.pi/2) - dy * math.cos(-math.pi/2)
        left_ext = (lx * correction + middle[0], ly * correction + middle[1])

        #Out of bounds indicator 
        r = 0 
        l = 0 

        # Walk right
        while True:
            grad = d2.d2grad(right_ext, stroke, SqrtA)
            right_ext = (right_ext[0] + grad[0] * alpha,right_ext[1] + grad[1] * alpha) 
            pix = (int(right_ext[0]),int(right_ext[1]))

            if not (0 <= pix[0] < width and 0 <= pix[1] < height):
                print("Out of bounds")
                r = 1
                break

            if pixels[pix[0] + width* pix[1]] == 255:
                break

        # Walk left
        while True:
            grad = d2.d2grad(left_ext, stroke, SqrtA)
            left_ext = (left_ext[0] + grad[0] * alpha, left_ext[1] + grad[1] * alpha)
            pix = (int(left_ext[0]),int(left_ext[1]))

            if not (0 <= pix[0] < width and 0 <= pix[1] < height):
                print("Out of bounds (left)")
                l = 1
                break

            if pixels[pix[0]+ width* pix[1]] == 255:
                break
        
        if l==0 and r==0 :
            ans_x : tuple = (int(right_ext[0]),int(right_ext[1]))
            ans_y : tuple = (int(left_ext[0]),int(left_ext[1]))
            ans : tuple = (ans_x, ans_y)
            ribs.append(ans)

    return ribs

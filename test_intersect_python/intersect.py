from PIL import Image
import math
from d2_v2 import d2grad
from d2_v2 import getSqrtA

def distance(x,y):
    return (x[0]-y[0])**2 +  (x[1]-y[1])**2

def generate_points(p1, p2, nb_points, d, stroke):

    total_length = math.sqrt(distance(p2, p1))

    direction = ((p2[0] - p1[0]) / total_length, (p2[1] - p1[1]) / total_length)

    for i in range(nb_points):
        stroke.append(p1[0] + direction[0] * d * (i + 1), p1[1] + direction[1] * d * (i + 1))

def contour_detection(path_image): 
    img = Image.open(path_image).convert("L")
    if img is None:
        print("Error: Could not open or find the image!")
        return -1

    width, height = img.size
    pixels = img.load()

    threshold = 30 

    # Crée une nouvelle image pour les contours
    edges = Image.new("L", (width, height))
    edge_pixels = edges.load()

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            gx = abs(pixels[x + 1, y] - pixels[x - 1, y])
            gy = abs(pixels[x, y + 1] - pixels[x, y - 1])
            gradient = gx + gy
            edge_pixels[x, y] = 255 if gradient > threshold else 0
    
    print("contour terminé")
    return edges


def intersect(path_image, path_stroke, type):
    edges = contour_detection(path_image) 
    stroke = []

    try:
        with open(path_stroke, "r") as f:
            for line in f:
                x_str, y_str = line.strip().split()
                stroke.append((float(x_str), float(y_str)))
    except Exception as e:
        print("Error reading stroke:", e)
        return -1

    SqrtA = getSqrtA(stroke)

    width, height = edges.size
    pixels = edges.load()

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
            
            generate_points(stroke[i],stroke[i+1],nb_points, d, stroke_arranged)
        
    else :
        stroke_arranged = stroke
        
    for i in range(1, len(stroke_arranged) - 1):
        p1 = stroke_arranged[i]
        p2 = stroke_arranged[i + 1]
        middle = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)

        dx = p2[0] - middle[0]
        dy = middle[1] - p2[1]

        # Right direction
        rx = middle[0] + dx * math.cos(math.pi/2) + dy * math.sin(math.pi/2)
        ry = middle[1] + dx * math.sin(math.pi/2) - dy * math.cos(math.pi/2)
        right_ext = ((rx - middle[0]) * correction + middle[0],
                    (ry - middle[1]) * correction + middle[1])

        # Left direction
        lx = middle[0] + dx * math.cos(-math.pi/2) + dy * math.sin(-math.pi/2)
        ly = middle[1] + dx * math.sin(-math.pi/2) - dy * math.cos(-math.pi/2)
        left_ext = ((lx - middle[0]) * correction + middle[0],
                    (ly - middle[1]) * correction + middle[1])

        # Walk right
        while True:
            grad = d2grad(right_ext, stroke, SqrtA)
            right_ext = (right_ext[0] + grad[0] * alpha, right_ext[1] + grad[1] * alpha)
            pix = (int(right_ext[0]), int(right_ext[1]))

            if not (0 <= pix[0] < width and 0 <= pix[1] < height):
                print("Out of bounds (right)")
                break

            # Marque les points visités en gris (128)
            if pixels[pix[0], pix[1]] != 255:
                pixels[pix[0], pix[1]] = 128

            if pixels[pix[0], pix[1]] == 255:
                break

        # Walk left
        while True:
            grad = d2grad(left_ext, stroke, SqrtA)
            left_ext = (left_ext[0] + grad[0] * alpha, left_ext[1] + grad[1] * alpha)
            pix = (int(left_ext[0]), int(left_ext[1]))

            if not (0 <= pix[0] < width and 0 <= pix[1] < height):
                print("Out of bounds (left)")
                break

            if pixels[pix[0], pix[1]] != 255:
                pixels[pix[0], pix[1]] = 128

            if pixels[pix[0], pix[1]] == 255:
                break

        ribs.append((right_ext, left_ext))

    # Sauvegarde facultative pour visualisation
    edges.save("edges_with_ribs.png")  # tu peux changer le chemin

    return len(ribs)

intersect("image.jpg","arc_stroke.txt",1)
from PIL import Image
import math
import d2grad 


def contour_detection(path_image): 

    # Charge l'image en niveaux de gris
    img = Image.open(path_image).convert("L")
    if img is None:
        print("Error: Could not open or find the image!")
        return -1

    width, height = img.size
    pixels = img.load()

    # Crée une nouvelle image pour les contours
    edges = Image.new("L", (width, height))
    edge_pixels = edges.load()

    # Détection simple : différence entre pixels voisins
    for y in range(1, height - 1):
        for x in range(1, width - 1):

            # Gradient approximatif (Sobel simplifié)
            gx = abs(pixels[x + 1, y] - pixels[x - 1, y])
            gy = abs(pixels[x, y + 1] - pixels[x, y - 1])
            gradient = gx + gy

            # Seuil de détection des bords réglables 
            edge_pixels[x, y] = 255 if gradient > 30 else 0

    return edges



def intersect(path_image, stroke, pRibs):

    edges = contour_detection(path_image) 

    width, height = edges.size
    pixels = edges.load()

    ribs = []
    alpha = 2.0
    correction = 10.0


    for i in range(0, len(stroke) - 1, 3):

        #Init of the two first points close to stroke point for determining the left and right point of the rib

        middle = (stroke[i] + stroke[i + 1]) / 2.0

        dx = stroke[i + 1].get_x() - middle.get_x()
        dy = middle.get_y() - stroke[i + 1].get_y()

        # Right
        rx = middle.get_x() + dx * math.cos(math.pi/2) + dy * math.sin(math.pi/2)
        ry = middle.get_y() + dx * math.sin(math.pi/2) - dy * math.cos(math.pi/2)
        right_ext = ((rx, ry) - middle) * correction + middle

        # Left
        lx = middle.get_x() + dx * math.cos(-math.pi/2) + dy * math.sin(-math.pi/2)
        ly = middle.get_y() + dx * math.sin(-math.pi/2) - dy * math.cos(-math.pi/2)
        left_ext = ((lx, ly) - middle) * correction + middle

        # Walk right
        while True:
            grad = d2grad(right_ext, stroke)
            right_ext = right_ext + grad * alpha
            pix = (int(right_ext[0]),int(right_ext[1]))

            if not (0 <= pix.get_x() < width and 0 <= pix.get_y() < height):
                print("Out of bounds")
                break

            if pixels[pix.get_x(), pix.get_y()] == 255:
                break

        # Walk left
        while True:
            grad = d2grad(left_ext, stroke)
            left_ext = left_ext + grad * alpha
            pix = (int(left_ext[0]),int(left_ext[1]))

            if not (0 <= pix.get_x() < width and 0 <= pix.get_y() < height):
                print("Out of bounds (left)")
                break

            if pixels[pix.get_x(), pix.get_y()] == 255:
                break

        ribs.append((right_ext.toint(), left_ext.toint()))

    for i, (r, l) in enumerate(ribs):
        pRibs[i] = {
            'x1': r[0], 'y1': r[1],
            'x2': l[0], 'y2': l[1]
        }

    return len(ribs)
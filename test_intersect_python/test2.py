from PIL import Image
from PIL import ImageFilter
import math

import os
print("Chemin absolu attendu :", os.path.abspath("girafe.jpg"))

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


def contour_detection(path_image, ignore_zones: list[list[tuple]]):
    # Charge l'image en niveaux de gris
    img = Image.open(path_image).convert("L")
    img = img.filter(ImageFilter.GaussianBlur(radius=7))  # Ajuste le radius selon ton image
    img.show()
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

            # Vérifie si (x, y) est dans une des zones à ignorer
            ignore = any(point_in_poly(x, y, zone) for zone in ignore_zones)
            if ignore:
                edge_pixels[x, y] = 0
                continue


            gx = abs(pixels[x + 1, y] - pixels[x - 1, y])
            gy = abs(pixels[x, y + 1] - pixels[x, y - 1])
            gradient = gx + gy
            edge_pixels[x, y] = 255 if gradient > 7 else 0

    return edges

# Appel avec affichage
img = Image.open("/Users/timotheefevrier/Desktop/3d-modeling/test_intersect_python/girafe.jpg")
img.show()
edges = contour_detection("/Users/timotheefevrier/Desktop/3d-modeling/test_intersect_python/girafe.jpg")
if isinstance(edges, Image.Image):
    edges.show()

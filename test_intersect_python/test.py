from PIL import Image
from PIL import ImageFilter
import math

import os
print("Chemin absolu attendu :", os.path.abspath("girafe.jpg"))

def contour_detection(path_image):
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

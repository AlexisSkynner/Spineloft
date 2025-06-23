from PIL import Image
import math

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
            gx = abs(pixels[x + 1, y] - pixels[x - 1, y])
            gy = abs(pixels[x, y + 1] - pixels[x, y - 1])
            gradient = gx + gy
            edge_pixels[x, y] = 255 if gradient > 30 else 0

    return edges

# Appel avec affichage
edges = contour_detection("image.jpg")
if isinstance(edges, Image.Image):
    edges.show()

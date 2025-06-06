from PIL import Image

# Charger l'image en niveaux de gris
img = Image.open("image.jpg").convert("L")
width, height = img.size
pixels = img.load()

# Créer une nouvelle image pour les contours
edges = Image.new("L", (width, height))
edge_pixels = edges.load()

# Détection basique : différence entre pixels voisins
for y in range(1, height - 1):
    for x in range(1, width - 1):
        # Gradient approximatif (Sobel simplifié)
        gx = abs(pixels[x + 1, y] - pixels[x - 1, y])
        gy = abs(pixels[x, y + 1] - pixels[x, y - 1])
        gradient = gx + gy

        # Seuillage pour détecter les bords
        edge_pixels[x, y] = 255 if gradient > 30 else 0

# Afficher le résultat
edges.show()
input("Appuyez sur Entrée pour quitter...")


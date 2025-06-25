from PIL import Image

def apply_box_blur(img: Image.Image, radius: int = 1) -> Image.Image:
    """
    Applique un flou simple (box blur) à une image en niveaux de gris sans dépendance externe.
    `radius` détermine la taille de la fenêtre : 1 = 3x3, 2 = 5x5, etc.
    """
    width, height = img.size
    pixels = img.load()

    # Crée une nouvelle image pour les résultats
    output = Image.new("L", (width, height))
    output_pixels = output.load()

    for y in range(height):
        for x in range(width):
            total = 0
            count = 0
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        total += pixels[nx, ny]
                        count += 1
            average = total // count
            output_pixels[x, y] = average

    return output

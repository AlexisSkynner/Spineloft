import math

# Centre du cercle
x_center = 650
y_center = 530
radius = 400

# Angle de départ et d'arrivée (anti-horaire)
start_angle = 3 * math.pi / 4   # ≈ 135°, en haut à gauche
end_angle = 5 * math.pi / 4     # ≈ 225°, en bas à gauche

# Nombre de points
num_points = 200

with open("arc_stroke.txt", "w") as f:
    for i in range(num_points):
        # interpolation linéaire entre les deux angles
        angle = start_angle + (end_angle - start_angle) * i / (num_points - 1)
        x = int(x_center + radius * math.cos(angle))
        y = int(y_center - radius * math.sin(angle))  # y inversé pour coordonnées écran
        f.write(f"{x} {y}\n")

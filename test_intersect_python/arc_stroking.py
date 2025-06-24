import math

# Centre du cercle
x_center = 430
y_center = 550
radius = 250  # Distance entre le centre et (600, 315)

# Angle de départ (en haut) vers l'angle de fin (en bas)
start_angle = -math.pi/2  # vers la droite (0°)
end_angle = math.pi / 2 # vers le bas (90°)

# Nombre de points
num_points = 500

with open("arc_stroke.txt", "w") as f:
    for i in range(num_points):
        angle = start_angle - (end_angle - start_angle) * i / (num_points - 1)
        x = int(x_center + radius * math.cos(angle))
        y = int(y_center - radius * math.sin(angle))
        f.write(f"{x} {y}\n")

from math import sin, cos

with open("stroke.txt", "w") as f:
    theta = 0
    n = 60
    for i in range(n + 1):
        f.write(f"{180 + int(50 * cos(theta))} {180 + int(50 * sin(theta))}")
        if i != n:
            f.write("\n")
        theta += 2.0 * 0.0314159
with open("stroke.txt", "w") as f:
    for i in range(2, 48):
        f.write(f"2 {i}")
        f.write("\n")
    for i in range(2, 48):
        f.write(f"{i} 48")
        f.write("\n")
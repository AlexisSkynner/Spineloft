with open("stroke.txt", "w") as f:
    for i in range(11):
        f.write(f"180 {130 + i * 10}")
        f.write("\n")
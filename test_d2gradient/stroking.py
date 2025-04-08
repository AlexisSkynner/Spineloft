with open("stroke.txt", "w") as f:
    for i in range(11):
        f.write(f"{130 + i * 10} {230 - i * 10}")
        f.write("\n")
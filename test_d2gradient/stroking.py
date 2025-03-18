with open("stroke.txt", "w") as f:
    for i in range(1, 11):
        f.write(f"200 {200 + i * 10}")
        f.write("\n")
# Création et écriture dans le fichier stroke.tkt
with open("stroke.txt", "w") as f:
    x = 315
    for _ in range(100):
        f.write(f"600 {x}\n")
        x += 2

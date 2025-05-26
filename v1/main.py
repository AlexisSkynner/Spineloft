from cffi import FFI
import math

ffi = FFI()

# Déclaration de la fonction C exposée
ffi.cdef("""
    typedef struct {
        float x_start, y_start;
        float x_end, y_end;
    } rib;

    typedef struct {
        int x, y;
    } pythonVec2;

    int intersect(const char* path, int nbPoints, pythonVec2* spine, rib* pRibs);
""")

# TODO : remplacer ça par ce que nous renvoie Blender
def fillSpine(spineSize, spine):
    # Centre du cercle
    x_center = 850
    y_center = 550
    radius = 250  # Distance entre le centre et (600, 315)

    # Angle de départ (en haut) vers l'angle de fin (en bas)
    start_angle = -math.pi/2  # vers la droite (0°)
    end_angle = math.pi / 2 # vers le bas (90°)

    with open("arc_stroke.txt", "w") as f:
        for i in range(spineSize):
            angle = start_angle - (end_angle - start_angle) * i / (spineSize - 1)
            spine[i].x = int(x_center + radius * math.cos(angle))
            spine[i].y = int(y_center - radius * math.sin(angle))

bufSize = 1000
C = ffi.dlopen("./libSpineLoft.dll") # remplacer par .dll ou .so ou .dylib selon l'OS

buf = ffi.new("rib[]", 2 * bufSize + 1)

spineSize = 100 # TODO : remplacer ça par le bon nombre de points dans la spine
spine = ffi.new("pythonVec2[]", spineSize)
fillSpine(spineSize, spine)

nbRibs = C.intersect(b"image.jpg", ffi.cast("int", spineSize), spine, buf)

for i in range(nbRibs):
    print(buf[i].x_start, buf[i].y_start)
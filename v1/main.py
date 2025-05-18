from cffi import FFI

ffi = FFI()

# Déclaration de la fonction C exposée
ffi.cdef("""
    typedef struct {
        float x_start, y_start;
        float x_end, y_end;
    } rib;

    int intersect(const char* path, rib* pRibs);
""")

nbPoints = 1000
C = ffi.dlopen("./libSpineLoft.dylib") # remplacer par le nom de la librairie créée

buf = ffi.new("rib[]", 2 * nbPoints + 1)
nbRibs = C.intersect(b"image.jpg", buf)

for i in range(nbRibs):
    print(buf[i].x_start, buf[i].y_start)
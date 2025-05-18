#ifndef INTERFACE_H
#define INTERFACE_H

extern "C" {

// Un rib est un segment (donc deux coordonnées pour début / fin)
typedef struct {
    float x_start, y_start;
    float x_end, y_end;
} rib;

/// @param path nom de l'image à ouvrir et transformer (ex : "image.png")
/// @param pRibs buffer qui contiendra les ribs renvoyés, doit être alloué avant appel !!!
/// @returns le nombre de ribs créés
int intersect(const char* path, rib* pRibs);
}

#endif
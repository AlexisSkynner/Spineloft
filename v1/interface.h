#ifndef INTERFACE_H
#define INTERFACE_H

extern "C" {

// Un rib est un segment (donc deux coordonnées pour début / fin)
typedef struct {
    float x_start, y_start;
    float x_end, y_end;
} rib;

typedef struct {
    int x, y;
} pythonVec2;

/// @param path nom de l'image à ouvrir et transformer (ex : "image.png")
/// @param nbPoints nombre de points dans la spine d'entrée
/// @param spine tableau de taille nbPoints, points formant la spine d'entrée  
/// @param pRibs buffer qui contiendra les ribs renvoyés, doit être alloué avant appel !!!
/// @returns le nombre de ribs créés
int intersect(const char* path, int nbPoints, pythonVec2* spine, rib* pRibs);
}

#endif
#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // Charger l'image en niveaux de gris
    cv::Mat image = cv::imread("image.jpg", cv::IMREAD_GRAYSCALE);
    
    // Vérifier que l'image est bien chargée
    if (image.empty()) {
        std::cerr << "Erreur : Impossible de charger l'image !" << std::endl;
        return -1;
    }

    // Définir les nouvelles dimensions ou un facteur d'échelle
    double scaleFactor = 0.2;  // Facteur de mise à l'échelle (50% de la taille originale)
    cv::Mat resizedImage;

    // Redimensionner l'image avec un facteur d'échelle
    cv::resize(image, resizedImage, cv::Size(), scaleFactor, scaleFactor, cv::INTER_LINEAR);

    // Vérifier que l'image redimensionnée est bien de type CV_8U
    if (resizedImage.depth() != CV_8U) {
        resizedImage.convertTo(resizedImage, CV_8U);
    }

    // Détection des contours avec Canny
    cv::Mat edges;
    cv::Canny(resizedImage, edges, 100, 200);

    // Afficher l'image
    cv::imshow("Contours", edges);

    // Attendre une touche avant de fermer les fenêtres
    cv::waitKey(0);
    return 0;
}
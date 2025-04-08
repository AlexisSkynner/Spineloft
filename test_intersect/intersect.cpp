#include <opencv2/opencv.hpp>
#include <iostream>
#include <cstdio> 
#include <vector>
#include <tuple>
#include <fstream>
#include <Vec2.h>


cv::Mat canny(cv::Mat image) {

    cv::Mat resizedImage;
    cv::resize(image, resizedImage, cv::Size(1920, 1080), 0, 0, cv::INTER_LINEAR);

    // Détection des contours avec Canny
    cv::Mat edges;
    cv::Canny(resizedImage, edges, 200, 200);

    int height = edges.rows;
    int width = edges.cols;


    // Afficher l'image
    cv::imshow("Edges", edges);
    cv::waitKey(0);

    return edges, height, width;
}




int main() {

    cv::Mat image = cv::imread("image.jpg", cv::IMREAD_COLOR);
    if (image.empty()) {
        std::cerr << "Error: Could not open or find the image!" << std::endl;
        return -1;
    }

    canny(image);

    //Stroke 

    std::vector<std::tuple<float, float>> stroke;
    float x, y;

    // Lire les deux colonnes
    while (file >> x >> y) {
        stroke.emplace_back(x, y);
    }

    file.close(); // Fermer le fichier

    //Gradient 
    cv::Mat gradient = d2_gradient(image);

    //Ribs
    std::vector<syd::tuple<int, int>> ribs;

    for (int i =0; i<=stroke.size(); i += 4){
        
    }

    return 0;

}
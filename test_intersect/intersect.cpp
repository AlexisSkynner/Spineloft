#include <opencv2/opencv.hpp>
#include <iostream>
#include <cstdio> 
#include <vector>
#include <tuple>
#include <fstream>
#include "external.hpp"


cv::Mat canny(cv::Mat image) {

    cv::Mat resizedImage;

    cv::resize(image, resizedImage, cv::Size(1920, 1080), 0, 0, cv::INTER_LINEAR);
    //resizedImage = image;

    // Détection des contours avec Canny
    cv::Mat edges;
    cv::Canny(resizedImage, edges, 300, 200);

    int height = edges.rows;
    int width = edges.cols;


    // Afficher l'image
    //cv::imshow("Edges", edges);
    std::cerr << "Canny done" << std::endl;

    return edges;
}


int main() {

    cv::Mat image = cv::imread("image.jpg", cv::IMREAD_COLOR);
    if (image.empty()) {
        std::cerr << "Error: Could not open or find the image!" << std::endl;
        return -1;
    }
    std::cerr << "Image charged" << std::endl;

    // Processing par Canny pour les edges
    cv::Mat edges = canny(image);

    // Créer un noyau de dilatation 3x3
    cv::Mat kernel = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3));

    // Dilater les contours
    cv::Mat edgesdilated;
    cv::dilate(edges, edgesdilated, kernel);
    std::cerr << "Dilate done" << std::endl;

    //Stroke 

    std::vector<Vec2> stroke;
    float x, y;

    std::ifstream file("stroke.txt");
    if (!file.is_open()) {
        std::cerr << "Error: Could not open the file!" << std::endl;
        return -1;
    }
    std::cerr << "File opened" << std::endl;

    // Lire les deux colonnes
    while (file >> x >> y) {
        stroke.emplace_back(x, y);
    }

    file.close(); // Fermer le fichier
    std::cerr << "File closed" << std::endl;

    //Ribs 
    std::vector<Vec2> ribs;
    cv::Mat imagetest;
    edgesdilated.copyTo(imagetest);

    for (int i = 0; i < stroke.size(); i+=3) {
        std::cerr << "Etude du vecteur" << i << std::endl;

        uchar pixelvalue;
        
        Vec2 extremity = stroke[i];
        imagetest.at<uchar>(extremity.get_y(), extremity.get_x()) = 150;

        const double alpha = 2.0;

        do {

            Vec2 gradient = d2grad(extremity,stroke);
            extremity = (extremity + gradient * alpha).toint();

            if ( extremity.get_x() < 0 or extremity.get_x() >= edgesdilated.cols or extremity.get_y() < 0 or  extremity.get_y() >= edgesdilated.rows) {
                std::cout << "Out of bounds" << std::endl;
                extremity = stroke[i];
                break;
            }

            pixelvalue = edgesdilated.at<uchar>(extremity.get_y(), extremity.get_x());
            imagetest.at<uchar>(extremity.get_y(), extremity.get_x()) = 150;

            cv::imshow("Pixel courant", imagetest);
            cv::waitKey(0);

        } while (pixelvalue != 255);
        
        ribs.emplace_back(extremity);
    }

}
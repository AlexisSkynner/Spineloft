#include <opencv2/opencv.hpp>
#include <iostream>
#include <cstdio> 
#include <vector>
#include <tuple>
#include <fstream>
#include <utility>  // Pour std::pair
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

    std::ifstream file("arc_stroke.txt");
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
    std::vector<std::pair<Vec2, Vec2>> ribs;
    cv::Mat imagetest;
    edgesdilated.copyTo(imagetest);

    for (int i = 0; i < stroke.size() -1; i+=3) {

        //Initialisation du point de stroke étudié

        std::cerr << "Etude du vecteur" << i << std::endl;

        uchar left_pixelvalue;
        uchar right_pixelvalue;
        
        const double alpha = 2.0;
        const double correction = 10;
       
        //Initialisation des points droits et gauches d'étude relatifs au point de stroke étudié

        Vec2 middleStroke = (stroke[i] + stroke[i+1]) / 2;
        std::cout << "Middle stroke : " << middleStroke.get_x() << ", " << middleStroke.get_y() << std::endl;

        Vec2 right_extremity_float = Vec2(middleStroke.get_x() + (stroke[i+1].get_x() - middleStroke.get_x()) * std::cos(M_PI/2) + (middleStroke.get_y() - stroke[i+1].get_y()) * std::sin(M_PI/2),
                                        middleStroke.get_y() + (stroke[i+1].get_x() - middleStroke.get_x()) * std::sin(M_PI/2) - (middleStroke.get_y() - stroke[i+1].get_y()) * std::cos(M_PI/2));

        right_extremity_float = (right_extremity_float - middleStroke)*correction + middleStroke;

        Vec2 left_extremity_float = Vec2(middleStroke.get_x() + (stroke[i+1].get_x() - middleStroke.get_x()) * std::cos(-M_PI/2) + (middleStroke.get_y() - stroke[i+1].get_y()) * std::sin(-M_PI/2),
                                        middleStroke.get_y() + (stroke[i+1].get_x() - middleStroke.get_x()) * std::sin(-M_PI/2) - (middleStroke.get_y() - stroke[i+1].get_y()) * std::cos(-M_PI/2));

        left_extremity_float = (left_extremity_float-middleStroke)*correction + middleStroke;

        Vec2 right_extremity = right_extremity_float.toint();
        Vec2 left_extremity = left_extremity_float.toint();

        imagetest.at<uchar>(middleStroke.toint().get_y(), middleStroke.toint().get_x()) = 100;
        cv::imshow("Pixel courant", imagetest);
        cv::waitKey(0);

        imagetest.at<uchar>(right_extremity.get_y(), right_extremity.get_x()) = 100;
       
        std::cout << "Right extremity : " << right_extremity.get_x() << ", " << right_extremity.get_y() << std::endl;

        cv::imshow("Pixel courant", imagetest);
        cv::waitKey(0);
      
        imagetest.at<uchar>(left_extremity.get_y(), left_extremity.get_x()) = 100;
        std::cout << "Left extremity : " << left_extremity.get_x() << ", " << left_extremity.get_y() << std::endl;

        cv::imshow("Pixel courant", imagetest);
        cv::waitKey(0);

        do {

            Vec2 right_gradient = d2grad(right_extremity,stroke);

            right_extremity = (right_extremity + right_gradient * alpha);
            Vec2 right_extremity_pixel = right_extremity.toint();

            if ( right_extremity_pixel.get_x() < 0 or right_extremity_pixel.get_x() >= edgesdilated.cols or right_extremity_pixel.get_y() < 0 or  right_extremity_pixel.get_y() >= edgesdilated.rows) {
                std::cout << "Out of bounds (right)" << std::endl;
                break;
            }
            imagetest.at<uchar>(right_extremity_pixel.get_y(), right_extremity_pixel.get_x()) = 150;

            right_pixelvalue = edgesdilated.at<uchar>(right_extremity_pixel.get_y(), right_extremity_pixel.get_x());

            //cv::imshow("Pixel courant", imagetest);
            //cv::waitKey(0);

        } while (right_pixelvalue != 255 );
        
        do {

            Vec2 left_gradient = d2grad(left_extremity,stroke);

            left_extremity = (left_extremity + left_gradient * alpha);
            Vec2 left_extremity_pixel = left_extremity.toint();

            if ( left_extremity_pixel.get_x() < 0 or left_extremity_pixel.get_x() >= edgesdilated.cols or left_extremity_pixel.get_y() < 0 or  left_extremity_pixel.get_y() >= edgesdilated.rows) {
                std::cout << "Out of bounds (left)" << std::endl;
                break;
            }
            imagetest.at<uchar>(left_extremity_pixel.get_y(), left_extremity_pixel.get_x()) = 150;

            left_pixelvalue = edgesdilated.at<uchar>(left_extremity_pixel.get_y(), left_extremity_pixel.get_x());

            //cv::imshow("Pixel courant", imagetest);
            //cv::waitKey(0);

        } while (left_pixelvalue != 255 );

        cv::imshow("Pixel courant", imagetest);
        cv::waitKey(0);
        
        ribs.emplace_back(std::make_pair(right_extremity, left_extremity));
    }

}
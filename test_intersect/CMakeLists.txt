cmake_minimum_required(VERSION 3.10)
project(test_intersect)

# Trouver OpenCV
find_package(OpenCV REQUIRED)

# Ajouter le fichier source
add_executable(intersect intersect.cpp d2.cpp)

# Lier OpenCV à l'exécutable
target_link_libraries(intersect ${OpenCV_LIBS})

# Inclure les headers d'OpenCV
include_directories(${OpenCV_INCLUDE_DIRS})

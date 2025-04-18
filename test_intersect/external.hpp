#pragma once

#include <vector>

class Vec2
{
private:
    float x, y;

public:
    Vec2(float __x, float __y)
        : x(__x), y(__y) {}

    inline float get_x() { return x; }
    inline float get_y() { return y; }

    Vec2 operator+(const Vec2 p);
    Vec2 operator-();
    Vec2 operator-(const Vec2 p);
    Vec2 operator*(const double a);
    Vec2 operator/(const double a);
    Vec2 toint();

    float length();
    float length2();
    float dot(Vec2 p);
    Vec2 sign();
};

float clamp(float x, float minVal, float maxVal);
float d2(Vec2 x, std::vector<Vec2> stroke);
Vec2 d2grad(Vec2 p, std::vector<Vec2> stroke);
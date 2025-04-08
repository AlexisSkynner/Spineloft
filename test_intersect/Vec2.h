#include <cmath>
#pragma once

class Vec2 {
    private:
        float x, y;
    
    public:
        Vec2(float __x, float __y)
            : x(__x), y(__y) {}
    
        float get_x() { return x; }
        float get_y() { return y; }
    
        Vec2 operator+(const Vec2 p) { return Vec2(x + p.x, y + p.y); }
        Vec2 operator-() { return Vec2(-x, -y); }
        Vec2 operator-(const Vec2 p) { return Vec2(x - p.x, y - p.y); }
        Vec2 operator*(const double a) { return Vec2(x * a, y * a); }
        Vec2 operator/(const double a) { return Vec2(x / a, y / a); }
    
        float length()
        {
            return sqrt(x * x + y * y);
        }
    
        float length2()
        {
            return x * x + y * y;
        }
    
        float dot(Vec2 p)
        {
            return x * p.get_x() + y * p.get_y();
        }
    };
    
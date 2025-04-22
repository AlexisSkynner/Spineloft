#include <vector>
#include <cmath>
#include <stdexcept>

#include "external.hpp"

float Vec2::length()
{
    return sqrtf(x * x + y * y);
}

float Vec2::length2()
{
    return x * x + y * y;
}

float Vec2::dot(Vec2 p)
{
    return x * p.get_x() + y * p.get_y();
}

Vec2 Vec2::sign()
{
    return Vec2(x == 0.0 ? 1.0 : x / std::abs(x), y == 0.0 ? 1.0 : y / std::abs(y));
}

Vec2 Vec2::operator+(const Vec2 p) { return Vec2(x + p.x, y + p.y); }
Vec2 Vec2::operator-() { return Vec2(-x, -y); }
Vec2 Vec2::operator-(const Vec2 p) { return Vec2(x - p.x, y - p.y); }
Vec2 Vec2::operator*(const double a) { return Vec2(x * a, y * a); }
Vec2 Vec2::operator/(const double a) { return Vec2(x / a, y / a); }

Vec2 Vec2::toint() {
    return Vec2(int(std::round(x)), int(std::round(y)));
}

float clamp(float x, float minVal, float maxVal)
{
    if(x < minVal) return minVal;
    if(x > maxVal) return maxVal;
    return x;
}

float mix(float a, float b, float t)
{
    return a * (1.0 - t) + b * t;
}

float sdfSegment(Vec2 p, Vec2 a, Vec2 b)
{
    Vec2 ba = b - a;
    Vec2 pa = p - a;
    float h = clamp(pa.dot(ba) / ba.length2(), 0.0, 1.0);
    return (pa - ba * h).length();
}

float smin(float a, float b, float k)
{
    float h = clamp(0.5 + 0.5 * (a - b) / k, 0.0, 1.0);
    return mix(a, b, h) - k * h * (1.0 - h);
}

float d2(Vec2 x, std::vector<Vec2> stroke)
{
    const float k = 32.0;
    float locMin = 9876543210.0;
    float d;
    for (auto p_i = stroke.begin(); p_i != stroke.end() - 1; p_i++)
    {
        d = sdfSegment(x, *p_i, *(p_i + 1));
        locMin = smin(locMin, d, k);
    }
    if(std::isnan(locMin))
    {
        throw std::runtime_error("d2 renvoie nan");
        return 0;
    }
    return locMin;
}

Vec2 d2grad(Vec2 p, std::vector<Vec2> stroke)
{
    Vec2 dx = Vec2(5.0, 0.0);
    Vec2 dy = Vec2(0.0, 5.0);
    Vec2 res = Vec2((d2(p + dx, stroke) - d2(p, stroke)) / dx.length(), (d2(p + dy, stroke) - d2(p, stroke)) / dy.length());
    return res / res.length();
}
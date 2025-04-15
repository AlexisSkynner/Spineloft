#include <iostream>
#include <vector>
#include <cmath>

#include "../d2.hpp"

#include <opencv2/opencv.hpp>

/*
class Vec2
{
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
        return sqrtf(x * x + y * y);
    }

    float length2()
    {
        return x * x + y * y;
    }

    float dot(Vec2 p)
    {
        return x * p.get_x() + y * p.get_y();
    }

    Vec2 sign()
    {
        return Vec2(x == 0.0 ? 1.0 : x / std::abs(x), y == 0.0 ? 1.0 : y / std::abs(y));
    }
};
*/

bool is_float_zero(float x)
{
    const double epsilon = 0.00000000000001;
    return fabs(x) < epsilon;
}

float w(Vec2 x, float t, float a, float ux, float vx)
{
    return a * (t + ux) / sqrtf(a * vx);
}

Vec2 grad_w(Vec2 x, float t, float a, float ux, Vec2 q1, float vx, Vec2 grad_vx, float wxt)
{
    return -q1 / sqrtf(a * vx) + grad_vx * wxt / (2.0 * vx);
}

float I(Vec2 x, float t, float a, float ux, float vx)
{
    if (is_float_zero(vx))
    {
        return -1.0 / (a * (t + ux));
    }
    else
    {
        return atan(w(x, t, a, ux, vx)) / sqrtf(a * vx);
    }
}

Vec2 I_grad(Vec2 x, float t, float a, float ux, Vec2 q1, float vx, Vec2 grad_vx)
{
    if (is_float_zero(vx))
    {
        return -q1 / ((a * (t + ux)) * (a * (t + ux)));
    }
    else
    {
        float wxt = w(x, t, a, ux, vx);
        return grad_w(x, t, a, ux, q1, vx, grad_vx, wxt) * (1.0 / sqrtf(a * vx)) / (1.0 + pow(wxt, 2.0)) - ((grad_vx * a * atan(wxt)) / pow(2.0 * a * vx, 1.5));
    }
}

Vec2 d2_grad(Vec2 x, std::vector<Vec2> stroke)
{
    float A = 0.0;
    Vec2 sum_num = Vec2(0.0, 0.0);
    float sum_denom = 0.0;

    for (auto it = stroke.begin(); it != stroke.end() - 2; it++)
    {
        Vec2 pi_diff = *(it + 1) - *it;
        float dist = pi_diff.length();

        Vec2 q0x = x - *it;
        Vec2 q1 = pi_diff / pi_diff.length();

        float a = q1.length2();
        float bx = -2.0 * q0x.dot(q1);
        float cx = q0x.dot(q0x);
        Vec2 grad_cx = q0x * 2.0;

        float ux = bx / (2.0 * a);
        Vec2 grad_ux = -q1 / a;

        float vx = cx - a * ux * ux;
        Vec2 grad_vx = grad_cx - grad_ux * 2.0 * a * ux;

        A += dist;

        Vec2 dnum = I_grad(x, dist, a, ux, q1, vx, grad_vx) - I_grad(x, 0.0, a, ux, q1, vx, grad_vx);
        sum_num = sum_num + dnum;

        float ddenom = I(x, dist, a, ux, vx) - I(x, 0.0, a, ux, vx);
        sum_denom += ddenom;
    }

    return sum_num * (-sqrtf(A) / 2.0 * pow(sum_denom, 1.5));
}

template <typename T>
float integrate(T &f, float a, float b)
{
    const float dt = 0.01;
    float ans = 0.;
    float t = a;
    while (t < b)
    {
        auto f_t = f(t);
        ans += dt * (f_t + 0.5 * (f(t + dt) - f_t));
        t += dt;
    }
    return ans;
}

float d2a(Vec2 x, std::vector<Vec2> stroke)
{
    float A = 0.;
    float sumOfIntegrals = 0.;

    for (auto p_i = stroke.begin(); p_i != stroke.end() - 1; p_i++)
    {
        Vec2 diff = *p_i - *(p_i + 1);
        float T = diff.length();
        A += T;

        Vec2 q0 = x - *p_i;
        Vec2 q1 = *(p_i + 1) - *p_i;
        q1 = q1 / q1.length();

        auto f = [&](float t)
        { return (q0 - q1 * t).length2() <= 0.0000000000001 ? 0. : 1.0 / (q0 - q1 * t).length2(); };
        sumOfIntegrals += integrate(f, 0., T);
    }
    return sqrtf(A / sumOfIntegrals);
}

float d2bis(Vec2 x, std::vector<Vec2> stroke)
{
    float A = 0.;
    float sumOfIs = 0.;

    for (auto p_i = stroke.begin(); p_i != stroke.end() - 2; p_i++)
    {
        Vec2 diff = *(p_i + 1) - *p_i;
        float T = diff.length();
        A += T;

        Vec2 q0x = x - *p_i;
        Vec2 q1 = diff / diff.length();

        float a = q1.length2();
        float bx = -2.0 * q0x.dot(q1);
        float cx = q0x.dot(q0x);
        Vec2 grad_cx = q0x * 2.0;

        float ux = bx / (2.0 * a);
        Vec2 grad_ux = -q1 / a;

        float vx = cx - a * ux * ux;
        Vec2 grad_vx = grad_cx - grad_ux * 2.0 * a * ux;

        sumOfIs += I(x, T, 1.0, ux, vx) - I(x, 0.0, 1.0, ux, vx);
    }
    return sqrtf(A / sumOfIs);
}




// float clamp(float x, float minVal, float maxVal)
// {
//     if(x < minVal) return minVal;
//     if(x > maxVal) return maxVal;
//     return x;
// }

// float mix(float a, float b, float t)
// {
//     return a * (1.0 - t) + b * t;
// }

// float sdfSegment(Vec2 p, Vec2 a, Vec2 b)
// {
//     Vec2 ba = b - a;
//     Vec2 pa = p - a;
//     float h = clamp(pa.dot(ba) / ba.length2(), 0.0, 1.0);
//     return (pa - ba * h).length();
// }

// float smin(float a, float b, float k)
// {
//     float h = clamp(0.5 + 0.5 * (a - b) / k, 0.0, 1.0);
//     return mix(a, b, h) - k * h * (1.0 - h);
// }

// float d2smin(Vec2 x, std::vector<Vec2> stroke)
// {
//     const float k = 32.0;
//     float locMin = 9876543210.0;
//     float d;
//     for (auto p_i = stroke.begin(); p_i != stroke.end() - 1; p_i++)
//     {
//         d = sdfSegment(x, *p_i, *(p_i + 1));
//         locMin = smin(locMin, d, k);
//     }
//     if(isnan(locMin))
//     {
//         std::cout << "NAN" << std::endl;
//         return 0;
//     }
//     return locMin;
// }

// The MIT License
// Copyright © 2018 Inigo Quilez
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

float cro( Vec2 a, Vec2 b ) { return a.get_x()*b.get_y()-a.get_y()*b.get_x(); }
float cos_acos_3( float x ) { x=sqrtf(0.5+0.5*x); return x*(x*(x*(x*-0.008972+0.039071)-0.107074)+0.576975)+0.5; }

float sdBezier(Vec2 pos, Vec2 A, Vec2 B, Vec2 C, Vec2 outQ)
{    
    Vec2 a = B - A;
    Vec2 b = A - B * 2.0 + C;
    Vec2 c = a * 2.0;
    Vec2 d = A - pos;

    // cubic to be solved (kx*=3 and ky*=3)
    float kk = 1.0/b.dot(b);
    float kx = kk * a.dot(b);
    float ky = kk * (2.0*a.dot(a)+d.dot(b))/3.0;
    float kz = kk * d.dot(a);      

    float res = 0.0;
    float sgn = 0.0;

    float p  = ky - kx*kx;
    float q  = kx*(2.0*kx*kx - 3.0*ky) + kz;
    float p3 = p*p*p;
    float q2 = q*q;
    float h  = q2 + 4.0*p3;

    if( h>=0.0 ) 
    {
        h = sqrtf(h);
        Vec2 x = (Vec2(h,-h)-Vec2(q,q))/2.0;

        Vec2 tmp = Vec2(powf(std::abs(x.get_x()), 1.0/3.0), powf(std::abs(x.get_y()), 1.0/3.0));
        Vec2 ss = x.sign();
        Vec2 uv = Vec2(ss.get_x() * tmp.get_x(), ss.get_y() * tmp.get_y());
        float t = uv.get_x() + uv.get_y();

		// from NinjaKoala - single newton iteration to account for cancellation
        t -= (t*(t*t+3.0*p)+q)/(3.0*t*t+3.0*p);
        
        t = clamp( t-kx, 0.0, 1.0 );
        Vec2  w = d+(c+b*t)*t;
        outQ = w + pos;
        res = w.length2();
    }
    else 
    {   
        float z = sqrtf(-p);
        float m = cos_acos_3( q/(p*z*2.0) );
        float n = sqrtf(1.0-m*m);
        n *= sqrtf(3.0);

        Vec2  t = Vec2(m+m,-n-m)*z-Vec2(kx,kx);
        float tx = clamp(t.get_x(), 0.0, 1.0);
        float ty = clamp(t.get_y(), 0.0, 1.0);
        Vec2  qx=d+(c+b*tx)*tx; float dx=qx.length2(), sx=cro(a+b*tx,qx);
        Vec2  qy=d+(c+b*ty)*ty; float dy=qy.length2(), sy=cro(a+b*ty,qy);
        if( dx<dy ) {res=dx;sgn=sx;outQ=qx+pos;} else {res=dy;sgn=sy;outQ=qy+pos;}

    }
    
    return sqrtf( res );
}

int main(int argc, char **argv)
{
    std::vector<Vec2> stroke;
    while (not std::cin.eof())
    {
        int x, y;
        std::cin >> x >> y;
        stroke.push_back(Vec2(x, y));
    }

    const int WIDTH = 360;
    const int HEIGHT = 360;

    // CV_8UC3 = 3 channels, 8 bit image depth
    // !!! OpenCV uses BGR instead of RGB !!!
    cv::Mat img(WIDTH, HEIGHT, CV_8UC3, cv::Scalar(0, 0, 0));

    cv::Vec3b pixel(0, 0, 0);

    for (int y = 0; y < img.rows; y++)
    {
        for (int x = 0; x < img.cols; x++)
        {
#if 0
// _____________________________________V1 : length de grad d2______________________________________

            Vec2 grad = d2_grad(Vec2(x, y), stroke);

            const int amp = 1000000;

            // int sineOfGradLength = static_cast<int>(255 * powf(sin(grad.length() * amp), 10.0));
            int sineOfGradLength = static_cast<int>(clamp(200 - grad.length() + 50 * sin(grad.length() * amp), 0.0, 255.0));

            // pixel[0] = std::min(255, static_cast<int>(fabs(grad.get_x()) * amp));
            pixel[0] = 0;
            pixel[1] = std::min(255, sineOfGradLength);
            pixel[2] = 0;
            // pixel[2] = std::min(255, static_cast<int>(fabs(grad.get_y()) * amp));

            // std::cout << grad.get_x() << " " << grad.get_y() << "  ";

#elif 0
// _____________________________________V2 : smoothmin des SDF de chaque segment______________________________________

            float d = d2smin(Vec2(x, y), stroke);
            
            // pixel[0] = static_cast<int>(clamp(200 - d + 50 * sin(d), 0.0, 255.0));// + 50 + 50 * sin(d)));
            pixel[0] = d;
            pixel[1] = d;
            pixel[2] = d;

            // pixel[1] = std::min(255, static_cast<int>(50 + 50 * sin(3.14159 * d)));
            // pixel[2] = std::min(255, static_cast<int>(50 + 50 * sin(3.14159 * d)));
#elif 0
// _____________________________________V3 : passe-bas d'un sdBézier______________________________________

            Vec2 p = Vec2(x / 128.0 - 1.0, y / 128.0 - 1.0);
            Vec2 v0 = Vec2(1.3,0.0);
            Vec2 v1 = Vec2(1.3,0.9);
            Vec2 v2 = Vec2(-0.3,-0.2);
            Vec2 kk = Vec2(0.0, 0.0);

            float smoothness = 0.5;
            Vec2 dpx = Vec2(0.1 * smoothness, 0.0);
            Vec2 dpy = Vec2(0.0, 0.1 * smoothness);

            float d1 = abs(sdBezier( p, v0,v1,v2, kk )); 
            float d2 = abs(sdBezier( p + dpx, v0,v1,v2, kk )); 
            float d3 = abs(sdBezier( p - dpx, v0,v1,v2, kk )); 
            float d4 = abs(sdBezier( p + dpy, v0,v1,v2, kk )); 
            float d5 = abs(sdBezier( p - dpy, v0,v1,v2, kk )); 
            float d6 = abs(sdBezier( p + dpx + dpy, v0,v1,v2, kk )); 
            float d7 = abs(sdBezier( p - dpx + dpy, v0,v1,v2, kk )); 
            float d8 = abs(sdBezier( p + dpx - dpy, v0,v1,v2, kk )); 
            float d9 = abs(sdBezier( p - dpx - dpy, v0,v1,v2, kk )); 
            float d = (d1 + d2 + d3 + d4 + d5 + d6 + d7 + d8 + d9) / 9.0;
            d *= 128.0;

            pixel[0] = static_cast<int>(clamp(200 - d + 50 * sin(d), 0.0, 255.0));// + 50 + 50 * sin(d)));
            pixel[1] = 0;
            pixel[2] = 0;
#elif 1
            float d = 255.0 * d2grad(Vec2(x, y), stroke).length();
            
            pixel[0] = static_cast<int>(clamp(200 - d + 50 * sin(d), 0.0, 255.0));// + 50 + 50 * sin(d)));
            pixel[1] = 0;
            pixel[2] = 0;
#endif
            img.at<cv::Vec3b>(cv::Point(x, y)) = pixel;
        }
    }

    cv::imshow("Gradient of d2 function at each point (blue : x, red : y)", img);

    cv::waitKey(0);

    return 0;
}

#include <iostream>
#include <vector>
#include <cmath>

#include <opencv2/opencv.hpp>

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

bool is_float_zero(float x)
{
    const double epsilon = 0.00000000000001;
    return fabs(x) < epsilon;
}

float w(Vec2 x, float t, float a, float ux, float vx)
{
    return a * (t + ux) / sqrt(a * vx);
}

Vec2 grad_w(Vec2 x, float t, float a, float ux, Vec2 q1, float vx, Vec2 grad_vx, float wxt)
{
    return -q1 / sqrt(a * vx) + grad_vx * wxt / (2.0 * vx);
}

float I(Vec2 x, float t, float a, float ux, float vx)
{
    if(is_float_zero(vx))
    {
        return -1.0 / (a * (t + ux));
    }
    else
    {
        return atan(w(x, t, a, ux, vx)) / sqrt(a * vx);
    }
}

Vec2 I_grad(Vec2 x, float t, float a, float ux, Vec2 q1, float vx, Vec2 grad_vx)
{
    if(is_float_zero(vx))
    {
        return -q1 / ((a * (t + ux)) * (a * (t + ux)));
    }
    else
    {
        float wxt = w(x, t, a, ux, vx);
        return grad_w(x, t, a, ux, q1, vx, grad_vx, wxt) * (1.0 / sqrt(a * vx)) / (1.0 + pow(wxt, 2.0))
             - ((grad_vx * a * atan(wxt)) / pow(2.0 * a * vx, 1.5));
    }
}

Vec2 d2_grad(Vec2 x, std::vector<Vec2> stroke)
{
    float A = 0.0;
    Vec2 sum_num = Vec2(0.0, 0.0);
    float sum_denom = 0.0;

    for(auto it = stroke.begin(); it != stroke.end() - 2; it++)
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

    return sum_num * (-sqrt(A) / 2.0 * pow(sum_denom, 1.5));
}


template<typename T>
float integrate(T& f, float a, float b)
{
    const float dt = 0.01;
    float ans = 0.;
    float t = a;
    while(t < b)
    {
        auto f_t = f(t);
        ans += dt * (f_t + 0.5 * (f(t + dt) - f_t));
        t += dt;
    }
    return ans;
}

float d2(Vec2 x, std::vector<Vec2> stroke)
{
    float A = 0.;
    float sumOfIntegrals = 0.;

    for(auto p_i = stroke.begin(); p_i != stroke.end() - 1; p_i++)
    {
        Vec2 diff = *p_i - *(p_i + 1);
        float T = diff.length();
        A += T;

        Vec2 q0 = x - *p_i;
        Vec2 q1 = *(p_i + 1) - *p_i;
        q1 = q1 / q1.length();

        auto f = [&](float t){ return (q0 - q1 * t).length2() <= 0.0000000000001 ? 0. : 1.0 / (q0 - q1 * t).length2(); };
        sumOfIntegrals += integrate(f, 0., T);
    }
    return sqrt(A / sumOfIntegrals);
}

float d2bis(Vec2 x, std::vector<Vec2> stroke)
{
    float A = 0.;
    float sumOfIs = 0.;

    for(auto p_i = stroke.begin(); p_i != stroke.end() - 2; p_i++)
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
    return sqrt(A / sumOfIs);
}

int main(int argc, char** argv)
{
    std::vector<Vec2> stroke;
    while(not std::cin.eof())
    {
        int x, y;
        std::cin >> x >> y;
        stroke.push_back(Vec2(x, y));
    }

    const int WIDTH = 360;
    const int HEIGHT = 360;

    // CV_8UC3 = 3 channels, 8 bit image depth
    // !!! OpenCV uses BGR instead of RGB !!!
    cv::Mat img(WIDTH, HEIGHT, CV_8UC3, cv::Scalar(0,0,0));

    cv::Vec3b pixel(0, 0, 0);

    for(int y=0;y<img.rows;y++)
    {
        for(int x=0;x<img.cols;x++)
        {
            Vec2 grad = d2_grad(Vec2(x, y), stroke);

            const int amp = 10000000;

            pixel[0] = std::min(255, static_cast<int>(fabs(grad.get_x()) * amp));
            // pixel[1] = std::min(255, static_cast<int>(grad.length() * amp));
            pixel[1] = 0;
            pixel[2] = std::min(255, static_cast<int>(fabs(grad.get_y()) * amp));

            // std::cout << grad.get_x() << " " << grad.get_y() << "  ";

            img.at<cv::Vec3b>(cv::Point(x,y)) = pixel;
        }
    }

    cv::imshow("Gradient of d2 function at each point (blue : x, red : y)", img);
    
    cv::waitKey(0);
    
    return 0;
}

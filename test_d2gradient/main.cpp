#include <iostream>
#include <vector>
#include <cmath>

#include <opencv2/opencv.hpp>

class Vec2 {
private:
    double x, y;

public:
    Vec2(double __x, double __y)
        : x(__x), y(__y) {}

    double get_x() { return x; }
    double get_y() { return y; }

    Vec2 operator+(const Vec2 p) { return Vec2(x + p.x, y + p.y); }
    Vec2 operator-() { return Vec2(-x, -y); }
    Vec2 operator-(const Vec2 p) { return Vec2(x - p.x, y - p.y); }
    Vec2 operator*(const double a) { return Vec2(x * a, y * a); }
    Vec2 operator/(const double a) { return Vec2(x / a, y / a); }

    double length()
    {
        return sqrt(x * x + y * y);
    }

    double length2()
    {
        return x * x + y * y;
    }

    double dot(Vec2 p)
    {
        return x * p.get_x() + y * p.get_y();
    }
};

bool is_double_zero(double x)
{
    const double epsilon = 0.00000000000001;
    return fabs(x) < epsilon;
}

double w(Vec2 x, double t, double a, double ux, double vx)
{
    return a * (t + ux) / sqrt(a * vx);
}

Vec2 grad_w(Vec2 x, double t, double a, double ux, Vec2 q1, double vx, Vec2 grad_vx, double wxt)
{
    return -q1 / sqrt(a * vx) + grad_vx * wxt / (2.0 * vx);
}

double I(Vec2 x, double t, double a, double ux, double vx)
{
    if(is_double_zero(vx))
    {
        return -1.0 / (a * (t + ux));
    }
    else
    {
        return atan(w(x, t, a, ux, vx)) / sqrt(a * vx);
    }
}

Vec2 I_grad(Vec2 x, double t, double a, double ux, Vec2 q1, double vx, Vec2 grad_vx)
{
    if(is_double_zero(vx))
    {
        return -q1 / ((a * (t + ux)) * (a * (t + ux)));
    }
    else
    {
        double wxt = w(x, t, a, ux, vx);
        return grad_w(x, t, a, ux, q1, vx, grad_vx, wxt) * (1.0 / sqrt(a * vx)) / (1.0 + pow(wxt, 2.0))
             - ((grad_vx * a * atan(wxt)) / pow(2.0 * a * vx, 1.5));
    }
}

Vec2 d2_grad(Vec2 x, std::vector<Vec2> stroke)
{
    double A = 0.0;
    Vec2 sum_num = Vec2(0.0, 0.0);
    double sum_denom = 0.0;

    for(auto it = stroke.begin(); it != stroke.end() - 1; it++)
    {
        Vec2 pi_diff = *(it + 1) - *it;
        double dist = pi_diff.length();

        Vec2 q0x = x - *it;
        Vec2 q1 = pi_diff / pi_diff.length();

        double a = q1.length2();
        double bx = -2.0 * q0x.dot(q1);
        double cx = q0x.dot(q0x);
        Vec2 grad_cx = q0x * 2.0;

        double ux = bx / (2.0 * a);
        Vec2 grad_ux = -q1 / a;

        double vx = cx - a * ux * ux;
        Vec2 grad_vx = grad_cx - grad_ux * 2.0 * a * ux;

        A += dist;

        Vec2 dnum = I_grad(x, dist, a, ux, q1, vx, grad_vx) - I_grad(x, 0.0, a, ux, q1, vx, grad_vx);
        sum_num = sum_num + (isnan(dnum.get_x()) or isnan(dnum.get_y()) ? Vec2(0.0, 0.0) : dnum);

        double ddenom = I(x, dist, a, ux, vx) - I(x, 0.0, a, ux, vx);
        sum_denom += isnan(ddenom) ? 0.0 : ddenom;
    }

    return sum_num * (-sqrt(A) / 2.0 * pow(sum_denom, 1.5));
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

    const int WIDTH = 500;
    const int HEIGHT = 500;

    // CV_8UC3 = 3 channels, 8 bit image depth
    // !!! OpenCV uses BGR instead of RGB !!!
    cv::Mat img(WIDTH, HEIGHT, CV_8UC3, cv::Scalar(0,0,0));

    cv::Vec3b pixel(0, 0, 0);
    for(int y=0;y<img.rows;y++)
    {
        for(int x=0;x<img.cols;x++)
        {
            Vec2 grad = d2_grad(Vec2(x, y), stroke);

            const int amp = 100000000;

            pixel[0] = static_cast<int>(amp * grad.get_y());
            pixel[1] = 0;
            pixel[2] = static_cast<int>(amp * grad.get_x());

            // std::cout << grad.get_x() << " " << grad.get_y() << "  ";

            img.at<cv::Vec3b>(cv::Point(x,y)) = pixel;
        }
    }

    cv::imshow("Gradient of d2 function at each point (r : x, b : y)", img);
    
    cv::waitKey(0);
    
    return 0;
}

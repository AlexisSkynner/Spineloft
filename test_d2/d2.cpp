#include <iostream>
#include <vector>
#include <cmath>

class Point {
private:
    int x, y;

public:
    Point(int __x, int __y)
        : x(__x), y(__y) {}

    Point operator+(const Point p)
    {
        return Point(x + p.x, y + p.y);
    }

    Point operator-(const Point p)
    {
        return Point(x - p.x, y - p.y);
    }

    Point operator*(const double a)
    {
        return Point(x * a, y * a);
    }

    Point operator/(const double a)
    {
        return Point(x / a, y / a);
    }

    double length()
    {
        return sqrt(x * x + y * y);
    }

    double length2()
    {
        return x * x + y * y;
    }
};

template<typename T>
double integrate(T& f, double a, double b)
{
    const double dt = 0.01;
    double ans = 0.;
    double t = a;
    while(t < b)
    {
        auto f_t = f(t);
        ans += dt * (f_t + 0.5 * (f(t + dt) - f_t));
        t += dt;
    }
    return ans;
}

double d2(Point x, std::vector<Point> stroke)
{
    double A = 0.;
    double sumOfIntegrals = 0.;

    for(auto p_i = stroke.begin(); p_i != stroke.end() - 1; p_i++)
    {
        Point diff = *p_i - *(p_i + 1);
        double T = diff.length();
        A += T;

        Point q0 = x - *p_i;
        Point q1 = *(p_i + 1) - *p_i;
        q1 = q1 / q1.length();

        auto f = [&](double t){ return (q0 - q1 * t).length2() <= 0 ? 0. : 1.0 / (q0 - q1 * t).length2(); };
        sumOfIntegrals += integrate(f, 0., T);
    }
    return sqrt(A / sumOfIntegrals);
}

// TODO : write d2 gradient function directly
// (the optimized one, with nabla I)
// then use OpenCV for output
int main(int argc, char** argv)
{
    std::vector<Point> stroke;
    while(not std::cin.eof())
    {
        int x, y;
        std::cin >> x >> y;
        stroke.push_back(Point(x, y));
    }

    for(int y = 0; y < 50; y++)
    {
        for(int x = 0; x < 50; x++)
        {
            double d = d2(Point(x, y), stroke);
            std::cout << d << " ";
        }
        std::cout << std::endl;
    }
    
    return 0;
}
#ifndef VEC2_H_
#define VEC2_H_
#include <ostream>
#include <cstdlib>  // for std::abs

struct Vec2 {
    int x;
    int y;

    Vec2(int xx=0, int yy=0) : x(xx), y(yy) {}

    Vec2 operator+(Vec2 other) const {
        return Vec2{x + other.x, y + other.y};
    }

    Vec2 operator+=(Vec2 other) {
        x += other.x;
        y += other.y;
        return *this;
    }

    bool operator<(Vec2 other) const {
        if (x != other.x) {
            return x < other.x;
        }
        return y < other.y;
    }

    // boundary values are inclusive
    bool within(int x_lower, int x_upper, int y_lower, int y_upper) const {
        return x >= x_lower && x <= x_upper &&
               y >= y_lower && y <= y_upper;
    }

    int manhattan_dist() const {
        return std::abs(x) + std::abs(y);
    }
};

std::ostream& operator<<(std::ostream& os, Vec2 vec) {
    os << '(' << vec.x << ", " << vec.y << ')';
    return os;
}

#endif  // VEC2_H_
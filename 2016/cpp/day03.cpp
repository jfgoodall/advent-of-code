#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

void parse_sides(std::string line, int sides[3]) {
    std::size_t pos{};
    sides[0] = std::stoi(line, &pos);
    line = line.substr(pos);
    sides[1] = std::stoi(line, &pos);
    line = line.substr(pos);
    sides[2] = std::stoi(line);
}

bool valid_triangle(int a, int b, int c) {
    auto long_side = std::max(a, std::max(b, c));
    return a+b+c - long_side > long_side;
}

void part1() {
    std::ifstream input("day03-input.dat");

    int count = 0;

    std::string line;
    while (std::getline(input, line)) {
        int sides[3];
        parse_sides(line, sides);

        if (valid_triangle(sides[0], sides[1], sides[2])) {
            ++count;
        }
    }

    std::cout << "Part 1: " << count << '\n';
}

void part2() {
    std::ifstream input("day03-input.dat");

    int count = 0;
    int sides[3][3] = {};

    std::string line;
    while (!input.eof()) {
        for (int i = 0; i < 3 && std::getline(input, line); ++i) {
            parse_sides(line, sides[i]);
        }

        if (!input.eof()) {
            for (int i = 0; i < 3; ++i) {
                if (valid_triangle(sides[0][i], sides[1][i], sides[2][i])) {
                    ++count;
                }
            }
        }
    }

    std::cout << "Part 2: " << count << '\n';
}

int main() {
    part1();
    part2();
}
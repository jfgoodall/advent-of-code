#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <optional>
#include "vec2.h"

int main() {
    std::ifstream input("day01-input.dat");
    
    Vec2 pos;
    Vec2 dir{0, 1};
    
    std::optional<int> part2;
    std::set<Vec2> visited;
    visited.insert(pos);

    std::string line;
    while (input >> line) {
        if (line[0] == 'R') {
            dir = Vec2{dir.y, -dir.x};
        } else {  // 'L'
            dir = Vec2{-dir.y, dir.x};
        }

        int steps = std::stoi(line.substr(1));
        for (int i = 0; i < steps; ++i) {
            pos += dir;

            if (visited.contains(pos) && !part2) {
                part2 = pos.manhattan_dist();
            }
            visited.insert(pos);
        }

    }

    std::cout << "Part 1: " << pos.manhattan_dist() << '\n';
    std::cout << "Part 2: " << *part2 << '\n';
}
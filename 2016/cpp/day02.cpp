#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <array>
#include "vec2.h"

template <typename T>
std::string find_code(const T& KEYPAD, Vec2 key) {
    std::ifstream input("day02-input.dat");
    std::ostringstream code;
    std::string line;
    while (input >> line) {
        for (auto ch : line) {
            Vec2 new_key;
            switch (ch) {
            case 'U': new_key = key + Vec2{-1, 0}; break;
            case 'D': new_key = key + Vec2{1, 0}; break;
            case 'L': new_key = key + Vec2{0, -1}; break;
            case 'R': new_key = key + Vec2{0, 1}; break;
            default: std::cout << "danger!\n";
            }

            if (new_key.within(0, KEYPAD.size()-1, 0, KEYPAD.size()-1) &&
                KEYPAD[new_key.x][new_key.y] != ' ') {
                key = new_key;
            }
        }
        code << KEYPAD[key.x][key.y];
    }
    return code.str();
}

int main() {
    std::array<std::string, 3> KEYPAD_1 = {"123", "456", "789"};
    Vec2 key{1, 1};  // #5
    std::cout << "Part 1: " << find_code(KEYPAD_1, key) << '\n';

    std::array<std::string, 5> KEYPAD_2 = {"  1  ", " 234 ", "56789", " ABC ", "  D  "};
    key = {2, 0};  // #5
    std::cout << "Part 2: " << find_code(KEYPAD_2, key) << '\n';
}
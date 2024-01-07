#include <cctype>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <array>
#include <algorithm>

constexpr unsigned kRows = 6;
constexpr unsigned kCols = 50;
using Screen = std::array<std::array<char, kCols>, kRows>;

Screen init_screen() {
    Screen screen;
    for (size_t i = 0; i < screen.size(); ++i) {
        for (size_t j = 0; j < screen[0].size(); ++j) {
            screen[i][j] = '.';
        }
    }
    return screen;
}

void print_screen(const Screen& screen) {
    for (size_t i = 0; i < screen.size(); ++i) {
        for (size_t j = 0; j < screen[0].size(); ++j) {
            std::cout << screen[i][j] << ' ';
        }
        std::cout << '\n';
    }
}

std::pair<int, int> extract_numbers(const std::string& s) {
    std::string digits = s;
    std::replace_if(digits.begin(), digits.end(),
                    [](auto ch) {return !isdigit(ch);}, ' ');

    size_t pos = 0;
    auto v1 = std::stoi(digits, &pos);
    auto v2 = std::stoi(digits.substr(pos));
    return {v1, v2};
}

void rect(Screen& screen, int width, int height) {
    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
            screen[i][j] = '#';
        }
    }
}

void rotate_column(Screen& screen, int col, int count) {
    for (int i = 0; i < count; ++i) {
        auto tmp = screen[screen.size()-1][col];
        for (int j = screen.size()-1; j > 0; --j) {
            screen[j][col] = screen[j-1][col];
        }
        screen[0][col] = tmp;
    }
}

void rotate_row(Screen& screen, int row, int count) {
    for (int i = 0; i < count; ++i) {
        auto tmp = screen[row][screen[0].size()-1];
        for (int j = screen[0].size()-1; j > 0; --j) {
            screen[row][j] = screen[row][j-1];
        }
        screen[row][0] = tmp;
    }
}

int count_lit(const Screen& screen) {
    int count = 0;
    for (int i = 0; i < screen.size(); ++i) {
        for (int j = 0; j < screen[0].size(); ++j) {
            if (screen[i][j] == '#') {
                ++count;
            }
        }
    }
    return count;
}

int main() {
    std::ifstream input("day08-input.dat");

    auto screen = init_screen();

    std::string line;
    while (std::getline(input, line)) {
        if (line.starts_with("rect")) {
            auto [width, height] = extract_numbers(line);
            rect(screen, width, height);
        } else if (line.starts_with("rotate column")) {
            auto [col, count] = extract_numbers(line);
            rotate_column(screen, col, count);
        } else if (line.starts_with("rotate row")) {
            auto [row, count] = extract_numbers(line);
            rotate_row(screen, row, count);
        } else {
            std::cout << "danger!\n";
        }
    }

    std::cout << "Part 1: " << count_lit(screen) << '\n';
    std::cout << "Part 2:\n";
    print_screen(screen);
}
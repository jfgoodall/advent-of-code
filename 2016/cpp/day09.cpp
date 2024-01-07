#include <iostream>
#include <fstream>
#include <string>
#include <string_view>
#include "string_view_utils.h"


std::size_t decompressed_size(const std::string_view& sv, bool recurse = false) {
    std::size_t pos = 0;
    std::size_t next = 0;
    std::size_t size = 0;

    while (pos < sv.size()) {
        if (sv[pos] == '(') {
            ++pos;
            auto m = svtoul(sv.substr(pos), &next);
            pos += next + 1;
            auto n = svtoul(sv.substr(pos), &next);
            pos += next + 1;

            auto segment_len = recurse ? decompressed_size(sv.substr(pos, m), true) : m;
            size += segment_len * n;

            pos += m;
        } else {
            ++size;
            ++pos;
        }
    }

    return size;
}

int main() {
    std::ifstream input{"day09-input.dat"};

    std::string line;
    std::getline(input, line);

    std::cout << "Part 1: " << decompressed_size(line) << '\n';
    std::cout << "Part 2: " << decompressed_size(line, true) << '\n';
}
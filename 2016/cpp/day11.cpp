#include <cctype>
#include <iostream>
#include <fstream>
#include <sstream>
#include <array>
#include <string>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include "string_utils.h"

struct State {
    int elevator;
    std::array<std::string, 4> floors;
};

void print_state(const State& state) {
    for (int i = 4; i > 0; --i) {
        std::cout << 'F' << i << (state.elevator==i-1 ? ": * " : ":   ") << state.floors[i-1] << '\n';
    }
}

State parse_input() {
    std::ifstream input{"day11-input.dat"};

    State state;
    state.elevator = 0;
    for (int i = 0; i < 4; ++i) {
        std::string line;
        std::getline(input, line);

        std::string stuff;
        if (line.find("nothing") == line.npos) {
            std::size_t pos = 0;
            while ((pos = line.find("generator", pos)) != line.npos) {
                auto space = line.find_last_of(' ', pos-2);
                stuff += std::toupper(line[space+1]);
                ++pos;
            }

            pos = 0;
            while ((pos = line.find("microchip", pos)) != line.npos) {
                auto space = line.find_last_of(' ', pos-2);
                stuff += std::tolower(line[space+1]);
                ++pos;
            }
        }

        std::sort(stuff.begin(), stuff.end());
        state.floors[i] = stuff;
    }
    return state;
}

inline bool is_chip(char c) {
    return c == std::tolower(c);
}

inline bool is_generator(char c) {
    return c == std::toupper(c);
}

bool valid_state(const State& state) {
    if (state.elevator < 0 or state.elevator > 3) {
        return false;
    }

    for (const auto& floor : state.floors) {
        bool has_generator = false;
        for (auto ch : floor) {
            if (is_generator(ch)) {
                has_generator = true;
                break;
            }
        }

        for (auto ch : floor) {
            if (is_chip(ch) &&
                has_generator &&
                !utils::str_contains(floor, std::toupper(ch))
            ) {
                return false;
            }
        }
    }
    return true;
}

std::string serialize_state(const State& state) {
    std::ostringstream oss;
    oss << state.elevator;
    for (const auto& floor : state.floors) {
        oss << '-' << floor;
    }
    return oss.str();
}

int main() {
    auto state = parse_input();
    print_state(state);

    std::cout << (int)valid_state(state) << '\n';
    std::cout << serialize_state(state) << '\n';

    std::unordered_set<std::string> seen;
    seen.insert(serialize_state(state));
}
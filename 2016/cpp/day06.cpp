#include <climits>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <optional>
#include <vector>

using Histogram = std::unordered_map<char, int>;
using HistogramList = std::vector<Histogram>;

std::string part1(const HistogramList& counters) {
    std::ostringstream msg;
    for (const auto& hist : counters) {
        int max_freq = 0;
        char letter = ' ';
        for (auto [ch, freq] : hist) {
            if (freq > max_freq) {
                max_freq = freq;
                letter = ch;
            }
        }
        msg << letter;
    }
    return msg.str();
}

std::string part2(const HistogramList& counters) {
    std::ostringstream msg;
    for (const auto& hist : counters) {
        int min_freq = INT_MAX;
        char letter = ' ';
        for (auto [ch, freq] : hist) {
            if (freq < min_freq) {
                min_freq = freq;
                letter = ch;
            }
        }
        msg << letter;
    }
    return msg.str();
}

int main() {
    std::ifstream input("day06-input.dat");

    std::optional<HistogramList> counters;

    std::string line;
    while (std::getline(input, line)) {
        if (!counters) {
            counters = HistogramList{};
            for (int i = 0; i < line.size(); ++i) {
                counters->emplace_back();
            }
        }

        for (size_t i = 0; i < line.size(); ++i) {
            const auto ch = line[i];
            auto& hist = (*counters)[i];
            if (hist.contains(ch)) {
                hist[ch] += 1;
            } else {
                hist[ch] = 1;
            }
        }
    }


    std::cout << "Part 1: " << part1(*counters) << '\n';
    std::cout << "Part 2: " << part2(*counters) << '\n';
}
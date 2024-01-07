#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <regex>
#include <unordered_map>
#include <vector>
#include <utility>
#include <algorithm>
#include <tuple>

using Room = std::tuple<std::string, int, std::string>;

std::vector<Room> parse_rooms() {
    std::ifstream input("day04-input.dat");

    const std::regex re{"([a-z\\-]+)-(\\d+)\\[(\\w+)]"};
    std::vector<Room> rooms;

    std::string line;
    while (std::getline(input, line)) {
        std::smatch match;
        if (std::regex_match(line, match, re)) {
            if (match.size() != 4) { std::cout << "danger!!\n"; }
            const auto encrypted = match.str(1);
            const auto sector_id = std::stoi(match[2]);
            const auto checksum = match.str(3);
            rooms.emplace_back(encrypted, sector_id, checksum);
        } else {
            std::cout << "danger!\n";
        }
    }
    return rooms;
}

bool is_real_room(const Room& room) {
    const auto& [encrypted, sector_id, checksum] = room;

    std::unordered_map<char, int> hist_map;
    for (auto ch : encrypted) {
        if (ch != '-') {
            if (hist_map.contains(ch)) {
                ++hist_map[ch];
            } else {
                hist_map[ch] = 1;
            }
        }
    }

    std::vector<std::pair<char, int>> hist_list;
    for (const auto& ch_count : hist_map) {
        hist_list.push_back(ch_count);
    }
    std::sort(
        hist_list.begin(), hist_list.end(),
        [](const auto a, const auto b) -> bool {
            if (a.second > b.second) {
                return true;
            } else if (a.second < b.second) {
                return false;
            }
            return a.first < b.first;
        });
    
    std::ostringstream most_common;
    for (int i = 0; i < 5; ++i) {
        most_common << hist_list[i].first;
    }
    return checksum == most_common.str();
}

int main() {
    auto rooms = parse_rooms();

    int sector_id_sum = 0;
    std::unordered_map<std::string, int> decrypted;
    for (const auto& room : rooms) {
        if (is_real_room(room)) {
            const auto& [encrypted, sector_id, checksum] = room;
            sector_id_sum += sector_id;

            std::ostringstream oss;
            for (auto ch : encrypted) {
                if (ch == '-') {
                    oss << ' ';
                } else {
                    oss << static_cast<char>(
                        ((ch-'a') + static_cast<char>(sector_id%26)) % 26 + 'a');
                }
                decrypted[oss.str()] = sector_id;
            }
        }
    }
    std::cout << "Part 1: " << sector_id_sum << '\n';
    std::cout << "Part 2: " << decrypted["northpole object storage"] << '\n';
}
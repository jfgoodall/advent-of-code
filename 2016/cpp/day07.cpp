#include <iostream>
#include <fstream>
#include <string>
#include <vector>

bool has_abba(const std::string& s) {
    bool abba = false;
    for (size_t i = 0; i < s.size()-3 && !abba; ++i) {
        abba = (s[i] == s[i+3] &&
                s[i+1] == s[i+2] &&
                s[i] != s[i+1]);
    }
    return abba;
}

bool supports_tls(const std::vector<std::string>& supernets,
                  const std::vector<std::string>& hypernets) {
    bool supports = false;
    for (const auto& s : supernets) {
        if (has_abba(s)) {
            supports = true;
            break;
        }
    }
    if (supports) {
        for (const auto& s : hypernets) {
            if (has_abba(s)) {
                supports = false;
                break;
            }
        }
    }
    return supports;
}

std::vector<std::string> find_abas(const std::vector<std::string>& supernets) {
    std::vector<std::string> abas;
    for (const auto& s : supernets) {
        for (size_t i = 0; i < s.size()-2; ++i) {
            if (s[i] == s[i+2] && s[i] != s[i+1]) {
                abas.emplace_back(s.substr(i, 3));
            }
        }
    }
    return abas;
}

bool supports_ssl(const std::vector<std::string>& supernets,
                  const std::vector<std::string>& hypernets) {
    auto abas = find_abas(supernets);
    for (const auto& hypernet : hypernets) {
        for (const auto& aba : abas) {
            char bab[] = {aba[1], aba[0], aba[1]};
            if (hypernet.find(bab) != hypernet.npos) {
                return true;
            }
        }
    }
    return false;
}

int main() {
    std::ifstream input("day07-input.dat");
    
    int tls_count = 0;
    int ssl_count = 0;
    std::string line;
    while (std::getline(input, line)) {
        std::vector<std::string> supernets;
        std::vector<std::string> hypernets;
    
        std::string::size_type start = 0;
        while (true) {
            auto end = line.find('[', start);
            if (end == line.npos) {
                supernets.emplace_back(line.substr(start));
                break;
            } else {
                supernets.emplace_back(line.substr(start, end-start));
                start = end + 1;
                end = line.find(']', start);
                hypernets.emplace_back(line.substr(start, end-start));
                start = end + 1;
            }
        }

        if (supports_tls(supernets, hypernets)) {
            ++tls_count;
        }
        if (supports_ssl(supernets, hypernets)) {
            ++ssl_count;
        }
    }

    std::cout << "Part 1: " << tls_count << '\n';
    std::cout << "Part 2: " << ssl_count << '\n';
}
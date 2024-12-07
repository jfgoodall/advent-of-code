#ifndef STRING_UTILS_H_
#define STRING_UTILS_H_
#include <string>
#include <string_view>
#include <vector>

namespace utils {

// split a string by character delimiter(s) into string_views; note
// the returned string_views share lifetime with the input string
std::vector<std::string_view> split(const std::string& s,
                                    const std::string& delim = " \t\n") {
    const auto sv = std::string_view(s);
    std::vector<std::string_view> results;

    std::size_t pos = 0;
    while (pos < s.length()) {
        pos = s.find_first_not_of(delim, pos);
        if (pos != s.npos) {
            auto end = s.find_first_of(delim, pos);
            if (end != s.npos) {
                results.push_back(sv.substr(pos, end-pos));
            } else {
                results.push_back(sv.substr(pos));
            }
            pos = end;
        }
    }
    return results;
}

bool str_contains(const std::string& s, char ch) {
    return s.find(ch) != s.npos;
}

}  // namespace utils

#endif  // STRING_UTILS_H_
#ifndef STRING_VIEW_UTILS_H_
#define STRING_VIEW_UTILS_H_
#include <charconv>
#include <stdexcept>
#include <string_view>

namespace impl {

// replicate std::stol and friends for std::string_view
template <typename T>
T svto_integer(const std::string_view& sv, std::size_t* pos = nullptr, int base = 10) {
    T result = 0;
    auto [ptr, ec] = std::from_chars(sv.data(), sv.data()+sv.size(), result, base);

    if (ec == std::errc::invalid_argument) {
        throw std::invalid_argument{"invalid argument"};
    } else if ( ec == std::errc::result_out_of_range) {
        throw std::out_of_range{"out of range"};
    }

    if (pos) {
        *pos = ptr - sv.data();
    }

    return result;
}

}  // namespace impl


int svtoi(const std::string_view& sv, std::size_t* pos = nullptr, int base = 10) {
    return impl::svto_integer<int>(sv, pos, base);
}
long svtol(const std::string_view& sv, std::size_t* pos = nullptr, int base = 10) {
    return impl::svto_integer<long>(sv, pos, base);
}
long long svtoll(const std::string_view& sv, std::size_t* pos = nullptr, int base = 10) {
    return impl::svto_integer<long long>(sv, pos, base);
}
int svtoui(const std::string_view& sv, std::size_t* pos = nullptr, int base = 10) {
    return impl::svto_integer<unsigned int>(sv, pos, base);
}
long svtoul(const std::string_view& sv, std::size_t* pos = nullptr, int base = 10) {
    return impl::svto_integer<unsigned long>(sv, pos, base);
}
long long svtoull(const std::string_view& sv, std::size_t* pos = nullptr, int base = 10) {
    return impl::svto_integer<unsigned long long>(sv, pos, base);
}

#endif  // STRING_VIEW_UTILS_H_
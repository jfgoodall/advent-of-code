#include <cassert>
#include <cstdint>
#include <climits>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <array>
#include <vector>

// https://stackoverflow.com/a/776523/8451814
static inline uint32_t rotl32 (uint32_t n, unsigned int c)
{
  const unsigned int mask = (CHAR_BIT*sizeof(n) - 1);  // assumes width is a power of 2.
  c &= mask;
  return (n<<c) | (n>>( (-c)&mask ));
}

std::array<uint8_t, 16> md5(const std::string& msg) {
    // https://en.wikipedia.org/wiki/MD5#Pseudocode
    static const std::array<uint32_t, 64> s = {
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
    };

    static const std::array<uint32_t, 64> K = {
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
    };

    uint32_t a0 = 0x67452301;
    uint32_t b0 = 0xefcdab89;
    uint32_t c0 = 0x98badcfe;
    uint32_t d0 = 0x10325476;

    std::vector<unsigned char> bits;
    bits.reserve(msg.size() + 64);
    for (auto ch : msg) {
        bits.push_back(ch);
    }

    bits.push_back(0x80);
    while (bits.size() % 64 != 56) {
        bits.push_back(0x00);
    }

    for (int i = 0; i < 8; ++i) {
        bits.push_back(msg.size()*CHAR_BIT >> CHAR_BIT*i & 0xff);
    }
    assert(bits.size() == 64);

    auto bits_iter = bits.begin();
    for (int chunk = 0; chunk < bits.size()/64; ++chunk) {
        std::array<uint32_t, 16> M{};
        for (int i = 0; i < M.size(); ++i) {
            decltype(M)::value_type word = 0;
            for (int j = 0; j < sizeof(decltype(M)::value_type); ++j, ++bits_iter) {
                word |= *bits_iter << CHAR_BIT*j;
            }
            M[i] = word;
        }
    
        uint32_t A = a0;
        uint32_t B = b0;
        uint32_t C = c0;
        uint32_t D = d0;

        for (int i = 0; i < 64; ++i) {
            uint32_t F = 0;
            uint32_t g = 0;
            if (i <= 15) {
                F = (B & C) | ((~B) & D);
                g = i;
            } else if (i <= 31) {
                F = (D & B) | ((~D) & C);
                g = (5*i + 1) % 16;
            } else if (i <= 47) {
                F = B ^ C ^ D;
                g = (3*i + 5) % 16;
            } else {
                F = C ^ (B | (~D));
                g = (7*i) % 16;
            }

            // Be wary of the below definitions of a,b,c,d
            F = F + A + K[i] + M[g];  // M[g] must be a 32-bit block
            A = D;
            D = C;
            C = B;
            B = B + rotl32(F, s[i]);
        }
        // Add this chunk's hash to result so far:
        a0 += A;
        b0 += B;
        c0 += C;
        d0 += D;
    }

    std::array<uint8_t, 16> digest;
    for (int i = 0; i < 4; ++i) {
        digest[0+i] = (a0 >> CHAR_BIT*i) & 0xff;
        digest[4+i] = (b0 >> CHAR_BIT*i) & 0xff;
        digest[8+i] = (c0 >> CHAR_BIT*i) & 0xff;
        digest[12+i] = (d0 >> CHAR_BIT*i) & 0xff;
    }
    return digest;
}

std::string md5_hex(const std::string& msg) {
    auto hash = md5(msg);

    std::ostringstream oss;
    for (int i = 0; i < hash.size(); ++i) {
        oss << std::setw(2) << std::hex << std::setfill('0') << static_cast<unsigned int>(hash[i]);
    }
    return oss.str();
}

void part1() {
    const std::string input{"wtnhxymk"};
    std::string password{"        "};
    uint64_t idx = 0;
    for (int i = 0; i < password.size(); ++i) {
        while (true) {
            auto hash = md5_hex(input + std::to_string(idx));
            ++idx;
            if (hash.starts_with("00000")) {
                password[i] = hash[5];
                break;
            }
        }
    }
    std::cout << "Part 1: " << password << '\n';
}

void part2() {
    const std::string input{"wtnhxymk"};
    std::string password{"        "};
    uint64_t idx = 0;
    for (int progress = 0; progress < password.size();) {
        while (true) {
            auto hash = md5_hex(input + std::to_string(idx));
            ++idx;
            if (hash.starts_with("00000")) {
                auto position = (hash[5] >= 'a') ? (hash[5] - 'a' + 10) : (hash[5] - '0');
                if (position < 8 && password[position] == ' ') {
                    password[position] = hash[6];
                    ++progress;
                    std::cout << progress << '\n';
                    break;
                }
            }
        }
    }
    std::cout << "Part 2: " << password << '\n';
}

int main() {
    part1();
    part2();
}
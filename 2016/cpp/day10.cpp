#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>
#include "string_utils.h"
#include "string_view_utils.h"

using BotList = std::vector<std::vector<int>>;
using InstructionList = std::vector<std::pair<int, int>>;
using JobList = std::vector<int>;

std::pair<std::size_t, std::size_t> count_bots_and_outputs(std::istream& input) {
    std::size_t bots = 0;
    std::size_t outputs = 0;

    std::string line;
    while (std::getline(input, line)) {
        if (line.starts_with("bot")) {
            ++bots;
            auto words = utils::split(line);
            outputs += (words[5] == "output");
            outputs += (words[10] == "output");
        }
    }

    input.clear();
    input.seekg(0);
    return {bots, outputs};
}

void give_chip(int chip, int bot, BotList& bots, JobList& jobs) {
    bots[bot].push_back(chip);
    if (bots[bot].size() == 2) {
        jobs.push_back(bot);
    }
}

std::tuple<BotList, InstructionList, JobList>
init_bots(std::istream& input) {
    const auto [num_bots, num_outputs] = count_bots_and_outputs(input);

    BotList bots{num_bots};
    InstructionList instructions{num_bots};
    JobList jobs;

    std::string line;
    while (std::getline(input, line)) {
        auto words = utils::split(line);
        if (words[0] == "value") {
            give_chip(utils::svtoi(words[1]), utils::svtoi(words[5]), bots, jobs);
        } else {
            auto bot = utils::svtoi(words[1]);
            auto low = utils::svtoi(words[6]);
            if (words[5] == "output") {
                low = -low - 1;
            }
            auto high = utils::svtoi(words[11]);
            if (words[10] == "output") {
                high = -high - 1;
            }
            instructions[bot] = {low, high};
        }
    }

    return {bots, instructions, jobs};
}

bool execute_instruction(const std::pair<int, int>& instruction,
                         const std::vector<int>& chips,
                         BotList& bots,
                         JobList& jobs,
                         std::vector<int>& outputs) {
    assert(chips.size() == 2);

    auto low = chips[0];
    auto high = chips[1];
    if (high < low) {
        std::swap(low, high);
    }

    auto [to_low, to_high] = instruction;
    if (to_low < 0) {
        outputs[-to_low-1] = low;
    } else {
        give_chip(low, to_low, bots, jobs);
    }
    if (to_high < 0) {
        outputs[-to_high-1] = high;
    } else {
        give_chip(high, to_high, bots, jobs);
    }

    return low == 17 && high == 61;
}

int main() {
    std::ifstream input{"day10-input.dat"};

    auto [bots, instructions, jobs] = init_bots(input);
    std::vector<int> outputs(bots.size());

    while (!jobs.empty()) {
        auto bot = jobs.back();
        jobs.pop_back();
        if (execute_instruction(instructions[bot], bots[bot], bots, jobs, outputs)) {
            std::cout << "Part 1: " << bot << '\n';
        }
    }
    std::cout << "Part 2: " << outputs[0]*outputs[1]*outputs[2] << '\n';
}
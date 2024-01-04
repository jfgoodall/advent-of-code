#!/usr/bin/env python3

def part1(time, buses):
    bus_ids = [i for i in buses if i is not None]
    def wait_time(bus):
        return ((time//bus + 1) * bus) - time
    wait_times = [(wait_time(b), b) for b in bus_ids]
    answer = min(wait_times, key=lambda x: x[0])
    return answer[0] * answer[1]

def part2_brute(buses):
    offsets = []
    for i, b in enumerate(buses):
        if b is not None:
            offsets.append((b, i))
    t = 0
    while True:
        t += buses[0]
        mods = [(t+off[1])%off[0] for off in offsets]
        if not any(mods):
            return t

def part2(buses):
    offsets = []
    for i, b in enumerate(buses):
        if b is not None:
            offsets.append((b, i))
    increment = 1
    factor = 1
    for bus, offset in offsets[1:]:
        while ((factor*buses[0]) + offset) % bus:
            factor += increment
        increment *= bus
    return buses[0] * factor

def parse_input(lines):
    t = int(lines[0])
    buses = []
    for i in lines[1].split(','):
        if i == 'x':
            buses.append(None)
        else:
            buses.append(int(i))
    return t, buses

def run_tests():
    test_input = """
939
7,13,x,x,59,x,31,19
""".strip().split('\n')
    time, buses = parse_input(test_input)
    assert part1(time, buses) == 295
    assert part2(buses) == 1068781;
    assert part2([17, None, 13, 19]) == 3417;
    assert part2([67, 7, 59, 61]) == 754018;
    assert part2([67, None, 7, 59, 61]) == 779210;
    assert part2([67, 7, None, 59, 61]) == 1261476;
    assert part2([1789, 37, 47, 1889]) == 1202161486;

if __name__ == '__main__':
    run_tests()
    with open('day13-input.dat') as infile:
        test_input = infile.read().strip().split('\n')
    time, buses = parse_input(test_input)
    print(f"Part 1: {part1(time, buses)}")
    print(f"Part 2: {part2(buses)}")

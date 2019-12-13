from fractions import gcd
from collections import defaultdict
import math

def map_to_coords(asteroid_map):
    coords = []
    for col in range(len(asteroid_map[0])):
        for row in range(len(asteroid_map)):
            if asteroid_map[row][col] == '#':
                coords.append((col, row))
    return coords

# original algorithm for part 1
def find_max_los(asteroid_map):
    coords = map_to_coords(asteroid_map)

    in_los = []
    for site in coords:
        def reduce_coord(coord):
            d = abs(gcd(*coord))
            if d:
                return (coord[0]/d, coord[1]/d)
            else:
                return (0, 0)
        vectors = [(site[0]-a[0], site[1]-a[1]) for a in coords]
        vectors = map(reduce_coord, vectors)
        in_los.append(len(set(vectors))-1)
    return max(in_los)

def offset_coords(coords, new_origin):
    return [(c[0]-new_origin[0], c[1]-new_origin[1]) for c in coords]

def trace_rays(asteroid_map):
    coords = map_to_coords(asteroid_map)

    rays = {}
    for site in coords:
        # site = (8, 3)
        shifted = offset_coords(coords, site)

        # {angle_from_north: [list_of_coords, ordered_by_dist_from_site]}
        site_rays = defaultdict(list)
        for coord in shifted:
            if coord == (0, 0):
                continue
            theta = math.atan2(coord[1], coord[0]) + math.pi/2.
            if theta < 0:
                theta += math.pi*2.
            site_rays[theta].append((coord[0]+site[0], coord[1]+site[1]))
        rays[site] = site_rays
    return rays

# better algorithm for part1 (returns coords of site)
def find_best_site(rays):
    best_site = max(rays.items(), key=lambda x: len(x[1]))
    return (len(best_site[1]), best_site[0])

def zap_asteroids(rays, site):
    zapped = []

    # sort asteroids in each ray by their distance to site
    def dist(coord):
        return (coord[0]-site[0])**2 + (coord[1]-site[1])**2
    for theta, coords in rays.items():
        rays[theta] = sorted(coords, key=dist)

    while rays:
        empty = []
        for theta in sorted(rays):
            zapped.append(rays[theta].pop(0))
            if not rays[theta]:
                empty.append(theta)
        for theta in empty:
            del rays[theta]
    return zapped


asteroid_map = [
    '.#..#',
    '.....',
    '#####',
    '....#',
    '...##',
]
assert find_max_los(asteroid_map) == 8
rays = trace_rays(asteroid_map)
assert find_best_site(rays) == (8, (3, 4))

asteroid_map = [
    '......#.#.',
    '#..#.#....',
    '..#######.',
    '.#.#.###..',
    '.#..#.....',
    '..#....#.#',
    '#..#....#.',
    '.##.#..###',
    '##...#..#.',
    '.#....####',
]
assert find_max_los(asteroid_map) == 33
rays = trace_rays(asteroid_map)
assert find_best_site(rays) == (33, (5, 8))

asteroid_map = [
    '#.#...#.#.',
    '.###....#.',
    '.#....#...',
    '##.#.#.#.#',
    '....#.#.#.',
    '.##..###.#',
    '..#...##..',
    '..##....##',
    '......#...',
    '.####.###.',
]
assert find_max_los(asteroid_map) == 35
rays = trace_rays(asteroid_map)
assert find_best_site(rays) == (35, (1, 2))

asteroid_map = [
    '.#..#..###',
    '####.###.#',
    '....###.#.',
    '..###.##.#',
    '##.##.#.#.',
    '....###..#',
    '..#.#..#.#',
    '#..#.#.###',
    '.##...##.#',
    '.....#.#..',
]
assert find_max_los(asteroid_map) == 41
rays = trace_rays(asteroid_map)
assert find_best_site(rays) == (41, (6, 3))

asteroid_map = [
    '.#..##.###...#######',
    '##.############..##.',
    '.#.######.########.#',
    '.###.#######.####.#.',
    '#####.##.#.##.###.##',
    '..#####..#.#########',
    '####################',
    '#.####....###.#.#.##',
    '##.#################',
    '#####.##.###..####..',
    '..######..##.#######',
    '####.##.####...##..#',
    '.#####..#.######.###',
    '##...#.##########...',
    '#.##########.#######',
    '.####.#.###.###.#.##',
    '....##.##.###..#####',
    '.#.#.###########.###',
    '#.#.#.#####.####.###',
    '###.##.####.##.#..##',
]
assert find_max_los(asteroid_map) == 210
rays = trace_rays(asteroid_map)
assert find_best_site(rays) == (210, (11, 13))
best_site = find_best_site(rays)[1]
zapped = zap_asteroids(rays[best_site], best_site)
gold = {
    1: (11,12), 2: (12,1), 3: (12,2), 10: (12, 8), 20: (16,0), 50: (16,9),
    100: (10,16), 199: (9,6), 200: (8,2), 201: (10,9), 299: (11,1)
}
for i in gold:
    assert zapped[i-1] == gold[i]

asteroid_map = [
    '.#..#..#..#...#..#...###....##.#....',
    '.#.........#.#....#...........####.#',
    '#..##.##.#....#...#.#....#..........',
    '......###..#.#...............#.....#',
    '......#......#....#..##....##.......',
    '....................#..............#',
    '..#....##...#.....#..#..........#..#',
    '..#.#.....#..#..#..#.#....#.###.##.#',
    '.........##.#..#.......#.........#..',
    '.##..#..##....#.#...#.#.####.....#..',
    '.##....#.#....#.......#......##....#',
    '..#...#.#...##......#####..#......#.',
    '##..#...#.....#...###..#..........#.',
    '......##..#.##..#.....#.......##..#.',
    '#..##..#..#.....#.#.####........#.#.',
    '#......#..........###...#..#....##..',
    '.......#...#....#.##.#..##......#...',
    '.............##.......#.#.#..#...##.',
    '..#..##...#...............#..#......',
    '##....#...#.#....#..#.....##..##....',
    '.#...##...........#..#..............',
    '.............#....###...#.##....#.#.',
    '#..#.#..#...#....#.....#............',
    '....#.###....##....##...............',
    '....#..........#..#..#.......#.#....',
    '#..#....##.....#............#..#....',
    '...##.............#...#.....#..###..',
    '...#.......#........###.##..#..##.##',
    '.#.##.#...##..#.#........#.....#....',
    '#......#....#......#....###.#.....#.',
    '......#.##......#...#.#.##.##...#...',
    '..#...#.#........#....#...........#.',
    '......#.##..#..#.....#......##..#...',
    '..##.........#......#..##.#.#.......',
    '.#....#..#....###..#....##..........',
    '..............#....##...#.####...##.',
]
rays = trace_rays(asteroid_map)
best = find_best_site(rays)
print("part 1: {} (@ {})".format(best[0], best[1]))
assert best == (276, (17, 22))
assert find_max_los(asteroid_map) == best[0]

zapped = zap_asteroids(rays[best[1]], best[1])
combined_coord = zapped[199][0]*100+zapped[199][1]
print("part 2: {} (@ {})".format(combined_coord, zapped[199]))
assert (combined_coord, zapped[199]) == (1321, (13, 21))

asteroid_map = [
    '.#....#####...#..',
    '##...##.#####..##',
    '##...#...#.#####.',
    '..#.....#...###..',
    '..#.#.....#....##',
]
rays = trace_rays(asteroid_map)
best_site = find_best_site(rays)[1]
zapped = zap_asteroids(rays[best_site], best_site)
gold = [
    (8, 1), (9, 0), (9, 1), (10, 0), (9, 2), (11, 1), (12, 1), (11, 2),
    (15, 1), (12, 2), (13, 2), (14, 2), (15, 2), (12, 3), (16, 4), (15, 4),
    (10, 4), (4, 4), (2, 4), (2, 3), (0, 2), (1, 2), (0, 1), (1, 1), (5, 2),
    (1, 0), (5, 1), (6, 1), (6, 0), (7, 0), (8, 0), (10, 1), (14, 0), (16, 1),
    (13, 3), (14, 3)
]
assert zapped == gold

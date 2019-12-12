from __future__ import print_function
import itertools
import numpy as np
import matplotlib.pyplot as plt

def dump_state(step, pos, vel):
    for body in range(np.shape(pos)[0]):
        print('{:4} : pos={:16} vel={}'.format(str(step), pos[body], vel[body]))
    print()

def calc_velocity(pos, vel):
    for pair in itertools.combinations(range(np.shape(pos)[0]), 2):
        for axis in range(np.shape(pos)[1]):
            if pos[pair[0]][axis] < pos[pair[1]][axis]:
                vel[pair[0]][axis] += 1
                vel[pair[1]][axis] -= 1
            elif pos[pair[0]][axis] > pos[pair[1]][axis]:
                vel[pair[0]][axis] -= 1
                vel[pair[1]][axis] += 1

def calc_position(pos, vel):
    pos += vel

def step_time(pos, vel):
    calc_velocity(pos, vel)
    calc_position(pos, vel)

def calc_energy(pos, vel):
    potential = abs(pos).sum(axis=1)
    kinetic = abs(vel).sum(axis=1)
    return sum(potential * kinetic)

def serialize_matrix(m):
    s = ''
    for axis1 in range(np.shape(m)[0]):
        for axis2 in range(np.shape(m)[1]):
            s += str(m[axis1][axis2])
            s += ','
    return s

def serialize_state(pos, vel):
    return serialize_matrix(pos) + serialize_matrix(vel)


pos = np.array((
    (-1, 0, 2),
    (2, -10, -7),
    (4, -8, 8),
    (3, 5, -1),
), dtype=np.int)
vel = np.zeros((4, 3), dtype=np.int)
for _ in range(10):
    step_time(pos, vel)
assert np.array_equal(pos, ((2,1,-3),(1,-8,0),(3,-6,1),(2,0,4)))
assert np.array_equal(vel, ((-3,-2,1),(-1,1,3),(3,2,-3),(1,-1,-1)))

pos = np.array((
    (-8, -10, 0),
    (5, 5, 10),
    (2, -7, 3),
    (9, -8, -3),
), dtype=np.int)
vel = np.zeros((4, 3), dtype=np.int)
for _ in range(100):
    step_time(pos, vel)
assert np.array_equal(pos, ((8,-12,-9),(13,16,-3),(-29,-11,-1),(16,-13,23)))
assert np.array_equal(vel, ((-7,3,0),(3,-11,-5),(-3,7,4),(7,1,1)))
assert calc_energy(pos, vel) == 1940

pos = np.array((
    (14, 4, 5),
    (12, 10, 8),
    (1, 7, -10),
    (16, -5, 3),
), dtype=np.int)
vel = np.zeros((4, 3), dtype=np.int)
for _ in range(1000):
    step_time(pos, vel)
print('part 1: {}'.format(calc_energy(pos, vel)))

# --- part 2 ---
def idx_of_value(seq, val):
    for i, v in enumerate(seq):
        if v == val:
            yield i

def calc_seq_len(seq):
    for idx in idx_of_value(seq[1:], seq[0]):
        period = idx+1
        if seq[:period] == seq[period:period*2]:
            print('found {}'.format(period))
            return period
    print('crap')
    return None

def find_common_period(pos, iterations=1000, start_pos=0):
    import multiprocessing as mp

    vel = np.zeros((4, 3), dtype=np.int)
    signals = [[] for _ in range(24)]
    print('sampling...')
    for _ in range(start_pos):
        step_time(pos, vel)
    for _ in range(iterations):
        for axis1 in range(np.shape(pos)[0]):
            for axis2 in range(np.shape(pos)[1]):
                idx = axis1*np.shape(pos)[1]+axis2
                signals[idx].append(pos[axis1][axis2])
                idx += len(signals)/2
                signals[idx].append(vel[axis1][axis2])
        step_time(pos, vel)
    print('calculating periods...')
    p = mp.Pool(mp.cpu_count())
    periods = set(p.map(calc_seq_len, signals))
    p.close()
    p.join()

    def lcm(seq):
        from fractions import gcd
        return reduce(lambda a, b: a * b / gcd(a, b), seq)

    return lcm(periods)

pos = np.array((
    (-1, 0, 2),
    (2, -10, -7),
    (4, -8, 8),
    (3, 5, -1),
), dtype=np.int)
assert find_common_period(pos) == 2772

pos = np.array((
    (-8, -10, 0),
    (5, 5, 10),
    (2, -7, 3),
    (9, -8, -3),
), dtype=np.int)
assert find_common_period(pos, iterations=100000) == 4686774924

pos = np.array((
    (14, 4, 5),
    (12, 10, 8),
    (1, 7, -10),
    (16, -5, 3),
), dtype=np.int)
# skip the first 10000 samples to let the intial conditions settle
period = find_common_period(pos, iterations=500000, start_pos=10000)
print('part 2: {}'.format(period))

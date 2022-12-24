import math


def popcount(n):
    return bin(n).count('1')

def lcm(a, b):
    return a * b // math.gcd(a, b)

#!/usr/bin/env python3

def validate_fields(pp):
    import re
    hgt_re = re.compile(r'^(\d+)(cm|in)$')
    hcl_re = re.compile(r'^#[0-9a-f]{6}$')
    pid_re = re.compile(r'^\d{9}$')

    valid = len(pp['byr']) == 4 and 1920 <= int(pp['byr']) <= 2002
    valid = valid and len(pp['iyr']) == 4 and 2010 <= int(pp['iyr']) <= 2020
    valid = valid and len(pp['eyr']) == 4 and 2020 <= int(pp['eyr']) <= 2030
    m = hgt_re.match(pp['hgt'])
    valid = valid and m and ((m.groups()[1] == 'cm' and 150 <= int(m.groups()[0]) <= 193) or
                             (m.groups()[1] == 'in' and 59 <= int(m.groups()[0]) <= 76))
    valid = valid and hcl_re.match(pp['hcl'])
    valid = valid and pp['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
    valid = valid and pid_re.match(pp['pid'])

    return valid

def solve(passports, strict=False):
    valid = 0
    for pp in passports:
        if {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}.issubset(pp.keys()):
            if not strict or validate_fields(pp):
                valid += 1
    return valid

def parse_input(lines):
    passports = []
    pp = {}
    for line in lines:
        line = line.strip()
        if line:
            for field in line.split():
                k, v = field.split(':')
                pp[k] = v
        elif pp:
            passports.append(pp)
            pp = {}
    if pp:
        passports.append(pp)
    return passports

def test_solve():
    test_input = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""
    passports = parse_input(test_input.split('\n'))
    assert solve(passports) == 2

if __name__ == '__main__':
    test_solve()
    with open('day04-input.dat') as infile:
        test_input = parse_input(infile)
    print(f"Part 1: {solve(test_input)}")
    print(f"Part 2: {solve(test_input, strict=True)}")

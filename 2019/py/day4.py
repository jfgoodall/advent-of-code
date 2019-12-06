from __future__ import print_function

def has_adjacent_matching(s):
    return s[0] == s[1] or s[1] == s[2] or s[2] == s[3] or s[3] == s[4] or s[4] == s[5]

def has_doubles(s):
    return ((s[0] == s[1]                  and s[0] != s[2]) or
            (s[1] == s[2] and s[1] != s[0] and s[1] != s[3]) or
            (s[2] == s[3] and s[2] != s[1] and s[2] != s[4]) or
            (s[3] == s[4] and s[3] != s[2] and s[3] != s[5]) or
            (s[4] == s[5] and s[4] != s[3]))

def consecutive_digits(s):
    return s[0] <= s[1] and s[1] <= s[2] and s[2] <= s[3] and s[3] <= s[4] and s[4] <= s[5]

valid = 0
for pw in range(271973, 785961+1):
    s = str(pw)
    if has_adjacent_matching(s) and consecutive_digits(s):
        valid += 1
print(valid)

valid = 0
for pw in range(271973, 785961+1):
    s = str(pw)
    if has_doubles(s) and consecutive_digits(s):
        valid += 1
print(valid)


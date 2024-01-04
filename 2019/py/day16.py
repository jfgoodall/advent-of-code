#/usr/bin/env python3

def str_to_array(number):
    return list(map(int, number))

def array_to_str(array):
    return ''.join(map(str, array))

def generate_pattern(level):
    while True:
        for n in (0, 1, 0, -1):
            for _ in range(level+1):
                yield n

# skip all of the 0's
def sum_nonzero_patterned_values(level, seq):
    accum = 0
    idx = level
    while idx < len(seq):
        for _ in range(level+1):
            accum += seq[idx]
            idx += 1
            if idx == len(seq):
                break
        idx += level + 1
        if idx >= len(seq):
            break
        for _ in range(level+1):
            accum -= seq[idx]
            idx += 1
            if idx == len(seq):
                break
        idx += level + 1
    return accum

def do_fft(signal):
    result = [None] * len(signal)
    for level in range(len(signal)):
        result[level] = abs(sum_nonzero_patterned_values(level, signal)) % 10
    return result

def multi_phase_fft(signal, num_phases, output_digits=8, use_message_offset=False):
    sig = str_to_array(signal)
    for _ in range(num_phases):
        print('\rphase {}/{}'.format(_+1, num_phases), end='')
        sig = do_fft(sig)
    print('\r                  \r', end='')
    if use_message_offset:
        offset = int(array_to_str(sig[:7]))
        return array_to_str(sig[offset:offset+output_digits])
    else:
        return array_to_str(sig[:output_digits])


assert multi_phase_fft('12345678', 4) == '01029498'
assert multi_phase_fft('80871224585914546619083218645595', 100) == '24176176'
assert multi_phase_fft('19617804207202209144916044189917', 100) == '73745418'
assert multi_phase_fft('69317163492948606335995924319873', 100) == '52432133'

with open('day16.dat') as f:
    signal = f.read().strip()
result = multi_phase_fft(signal, 100)
print("part 1: {}".format(result))
assert result == '59281788'

array = str_to_array(signal * 10000)
offset = int(signal[:7])
array = array[offset:]
for _ in range(100):
    print('\rphase {}/{}'.format(_+1, 100), end='')
    result = [None] * len(array)
    result[-1] = array[-1]
    for i in range(len(array)-2, -1, -1):
        result[i] = (result[i+1] + array[i]) %10
    array = result
print("\rpart 2: {}            ".format(array_to_str(array[:8])))

import collections


def load_data() :
    with open('data/input-day10.txt', 'r') as fp:
        jolts = [ int(jolt) for jolt in fp.readlines() ]
    jolts.append(0)
    jolts.append(max(jolts)+3)
    return sorted(jolts)


jolts = load_data()


diffs = [ jolts[i+1] - jolts[i] for i in range(0, len(jolts)-1) ]
jolts_1 = diffs.count(1)
jolts_3 = diffs.count(3)
print(jolts_1 * jolts_3)


calculated = dict()
def calculate_combinations(jolts) :
    last = jolts[-1]
    if last in calculated :
        return calculated[last]

    result = 0
    if len(jolts) < 3 :
        return 1

    if last - jolts[-2] <= 3 :
        result += calculate_combinations(jolts[:-1])
    if len(jolts) >= 3 and last - jolts[-3] <= 3 :
        result += calculate_combinations(jolts[:-2])
    if len(jolts) >= 4 and last - jolts[-4] <= 3 :
        result += calculate_combinations(jolts[:-3])
    calculated[last] = result
    return result


print(calculate_combinations(jolts))



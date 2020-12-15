with open('data/input-day15.txt', 'r') as fp :
    start = list(map(int, fp.readline().split(',')))


def findNth(n, data) :
    turn = len(data)
    lastSpoken = data[-1]
    previous = { value: turn+1 for turn, value in enumerate(data[:-1]) }

    while turn < n :
        if lastSpoken not in previous :
            previous[lastSpoken] = turn
            lastSpoken = 0
        else :
            diff = turn - previous[lastSpoken]
            previous[lastSpoken] = turn
            lastSpoken = diff
        turn += 1

    return lastSpoken


print('{}: {}th = {}'.format(start, 2020, findNth(2020, start)))
print('{}: {}th = {}'.format(start, 30000000, findNth(30000000, start)))

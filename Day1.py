
with open('data/input-day1.txt' , 'r') as f:
    values = list(map(int, f.readlines()))


def find_pair(values, sum) :
    for x in range(0, len(values)-1) :
        for y in range(x+1, len(values)) :
            if values[x]+values[y] == sum :
                return values[x], values[y]
    return None, None

x, y = find_pair(values, 2020)
print('{} * {} = {}'.format(x, y, x*y))


def find_triple(values, sum) :
    for x in range(0, len(values)-2) :
        for y in range(x+1, len(values)-1) :
            for z in range(y+1, len(values)) :
                if values[x]+values[y]+values[z] == sum :
                    return values[x], values[y], values[z]
    return None, None, None

x, y, z = find_triple(values, 2020)
print('{} * {} * {} = {}'.format(x, y, z, x*y*z))


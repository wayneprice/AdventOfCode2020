

class dataset3d :
    __neighbours = [(int(x/9) - 1, int(x/3) % 3 - 1, int(x % 3) - 1) for x in range(0, 27) if x != 13]

    def __init__(self, datafile) :
        with open(datafile, 'r') as fp :
            dataset = [[]]
            for line in fp :
                dataset[0].append([ c for c in line.strip()])
        self.__dataset = self.__copy_expand(dataset)


    @staticmethod
    def __copy_expand(dataset) :
        new_dataset = [[['.' for x in range(0, len(dataset[0][0]) + 2)] for y in range(0, len(dataset[0]) + 2)] for z in range(0, len(dataset) + 2)]
        for z in range(0, len(dataset)) :
            for y in range(0, len(dataset[z])) :
                for x in range(0, len(dataset[z][y])) :
                    new_dataset[z+1][y+1][x+1] = dataset[z][y][x]
        return new_dataset


    def iterate(self) :
        new_dataset = self.__copy_expand(self.__dataset)
        dataset = self.__copy_expand(self.__dataset)
        for z in range(1, len(dataset)-1) :
            for y in range(1, len(dataset[z])-1) :
                for x in range(1, len(dataset[z][y])-1) :
                    count = sum([1 if dataset[z+n[2]][y+n[1]][x+n[0]] == '#' else 0 for n in self.__neighbours])
                    if dataset[z][y][x] == '.' :
                        new_dataset[z][y][x] = '#' if count == 3 else '.'
                    elif dataset[z][y][x] == '#' :
                        new_dataset[z][y][x] = '#' if count in [2, 3] else '.'

        self.__dataset = new_dataset


    def get_active(self) :
        return sum([sum([sum([1 if c == '#' else 0 for c in y]) for y in z]) for z in self.__dataset])


    def print(self) :
        for z in range(0, len(self.__dataset)) :
            print('z={}'.format(z))
            for y in range(0, len(self.__dataset[z])) :
                print(''.join(self.__dataset[z][y]))
        print()


class dataset4d :
    __neighbours = [(int(x/27) % 3 - 1, int(x/9) % 3 - 1, int(x/3) % 3 - 1, x % 3 - 1) for x in range(0, 81) if x != 40]

    def __init__(self, datafile) :
        with open(datafile, 'r') as fp :
            dataset = [[[]]]
            for line in fp :
                dataset[0][0].append([ c for c in line.strip()])
        self.__dataset = self.__copy_expand(dataset)


    @staticmethod
    def __copy_expand(dataset) :
        new_dataset = [[[['.' for x in range(0, len(dataset[0][0][0]) + 2)] for y in range(0, len(dataset[0][0]) + 2)] for z in range(0, len(dataset[0]) + 2)] for w in range(0, len(dataset) + 2)]
        for w in range(0, len(dataset)) :
            for z in range(0, len(dataset[w])):
                for y in range(0, len(dataset[w][z])) :
                    for x in range(0, len(dataset[w][z][y])) :
                        new_dataset[w+1][z+1][y+1][x+1] = dataset[w][z][y][x]
        return new_dataset


    def iterate(self) :
        new_dataset = self.__copy_expand(self.__dataset)
        dataset = self.__copy_expand(self.__dataset)
        for w in range(1, len(dataset)-1) :
            for z in range(1, len(dataset[w]) - 1):
                for y in range(1, len(dataset[w][z])-1) :
                    for x in range(1, len(dataset[w][z][y])-1) :
                        count = sum([1 if dataset[w+n[3]][z+n[2]][y+n[1]][x+n[0]] == '#' else 0 for n in self.__neighbours])
                        if dataset[w][z][y][x] == '.' :
                            new_dataset[w][z][y][x] = '#' if count == 3 else '.'
                        elif dataset[w][z][y][x] == '#' :
                            new_dataset[w][z][y][x] = '#' if count in [2, 3] else '.'

        self.__dataset = new_dataset


    def get_active(self) :
        return sum([sum([sum([sum([1 if c == '#' else 0 for c in y]) for y in z]) for z in w]) for w in self.__dataset])



datafile = 'data/input-day17.txt'

dataset = dataset3d(datafile)
for iter in range(0, 6) :
    dataset.iterate()
print(dataset.get_active())

dataset = dataset4d(datafile)
for iter in range(0, 6) :
    dataset.iterate()
print(dataset.get_active())

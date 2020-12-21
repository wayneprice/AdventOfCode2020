import math


class Image :
    def __init__(self, index, image_data) :
        self.__index = index
        self.__data = image_data
        self.__set_edges()

    def __set_edges(self) :
        self.__leftIndex = ''.join([ x[0] for x in self.__data ])
        self.__rightIndex = ''.join([ x[-1] for x in self.__data ])
        self.__topIndex = self.__data[0]
        self.__bottomIndex = self.__data[-1]

    def rotateCW(self):
        data = []
        for row in range(0, len(self.__data)) :
            data.append('')
            for col in range(0, len(self.__data)) :
                data[row] += self.__data[len(self.__data)-col-1][row]
        self.__data = data
        self.__set_edges()

    def flipVertical(self) :
        self.__data = self.__data[::-1]
        self.__set_edges()

    def flipHorizontal(self) :
        for row in range(0, len(self.__data)) :
            self.__data[row] = self.__data[row][::-1]
        self.__set_edges()

    def trim(self) :
        self.__data = [ x[1:-1] for x in self.__data[1:-1]]
        self.__set_edges()

    def print(self) :
        print('Index', self.__index)
        print('\n'.join(self.__data))
        print()

    @property
    def index(self) :
        return self.__index

    @property
    def edge_indexes(self) :
        return [ self.__leftIndex, self.__rightIndex, self.__topIndex, self.__bottomIndex,
                 self.__leftIndex[::-1], self.__rightIndex[::-1], self.__topIndex[::-1], self.__bottomIndex[::-1]]

    @property
    def left_index(self):
        return self.__leftIndex

    @property
    def right_index(self):
        return self.__rightIndex

    @property
    def top_index(self):
        return self.__topIndex

    @property
    def bottom_index(self):
        return self.__bottomIndex

    @property
    def size(self) :
        return len(self.__data)

    @property
    def data(self) :
        return self.__data



def read_images(filename) :
    images = {}
    with open(filename, 'r') as fp :
        for line in fp :
            tile_index = int(line.split()[1].rstrip(':'))

            image_data = []
            for image_row in fp :
                image_row = image_row.rstrip()
                if not image_row :
                    break
                image_data.append(image_row)

            images[tile_index] = Image(tile_index, image_data)

    return images


def find_image_correlation(images) :
    # Setup set of all possible image edges (including flipped), and count the frequency of them
    edges = []
    for image in images.values() :
        edges.extend(image.edge_indexes)

    edge_frequency = { x: edges.count(x) for x in edges }

    # For all edges with a count of 1, these must be either edges or corners. Others, with a count
    # of 2 will be joining edges. Setup list of all tiles, and assign a count of edge sides
    image_edges = {}

    for index, image in images.items() :
        image_edges[index] = 8 - (edge_frequency[image.left_index] + edge_frequency[image.top_index] + edge_frequency[image.right_index] + edge_frequency[image.bottom_index])

    # Output image will be square, so setup a blank output
    result_size = int(math.sqrt(len(images)))
    result = []
    for row in range(0, result_size) :
        result.append([])
        for col in range(0, result_size) :
            result[row].append(0)

    # Start with a corner image for the top-left, and orient it correctly
    used_images = set()
    top_left = next(index for index, edges in image_edges.items() if edges == 2)
    while edge_frequency[images[top_left].left_index] != 1 or edge_frequency[images[top_left].top_index] != 1 :
        images[top_left].rotateCW()
    result[0][0] = top_left
    used_images.add(top_left)

    # Complete the top row
    for col in range(1, result_size) :
        for index, image in images.items() :
            if index in used_images :
                continue
            if images[result[0][col-1]].right_index in image.edge_indexes :
                while images[result[0][col-1]].right_index not in [ images[index].left_index, images[index].left_index[::-1]] :
                    images[index].rotateCW()
                if images[result[0][col-1]].right_index != images[index].left_index :
                    images[index].flipVertical()
                result[0][col] = index
                used_images.add(index)
                break

    # Complete the remaining rows using the row above
    for row in range(1, result_size) :
        for col in range(0, result_size) :
            for index, image in images.items():
                if index in used_images :
                    continue
                if images[result[row-1][col]].bottom_index in image.edge_indexes :
                    while images[result[row-1][col]].bottom_index not in [ images[index].top_index, images[index].top_index[::-1]] :
                        images[index].rotateCW()
                    if images[result[row-1][col]].bottom_index != images[index].top_index :
                        images[index].flipHorizontal()
                    result[row][col] = index
                    used_images.add(index)
                    break

    return result


def create_combined_image(correlation, images) :
    image_size = images[correlation[0][0]].size
    data = []
    for row in range(0, len(correlation)) :
        for y in range(0, image_size) :
            data.append(''.join([images[x].data[y] for x in correlation[row]]))

    return Image(0, data)


def find_sea_monsters(combined_image, sea_monster) :
    sea_monsters = []
    for flip in range(0, 2) :
        for rotate in range(0, 4) :
            for x in range(0, combined_image.size - len(sea_monster[0])) :
                for y in range(0, combined_image.size - len(sea_monster)) :
                    found = True
                    for sx in range(len(sea_monster[0])) :
                        if not found :
                            break
                        for sy in range(len(sea_monster)) :
                            if sea_monster[sy][sx] == '#' and combined_image.data[y+sy][x+sx] not in ['#', 'O'] :
                                found = False
                                break
                    if found :
                        for sy in range(len(sea_monster)):
                            row = list(combined_image.data[y + sy])
                            for sx in range(len(sea_monster[0])):
                                if sea_monster[sy][sx] == '#':
                                    row[x + sx] = 'O'
                            combined_image.data[y + sy] = ''.join(row)
                        sea_monsters.append((x, y))

            combined_image.rotateCW()
        combined_image.flipVertical()

    return sea_monsters


# Read images
images = read_images('data/input-day20.txt')

correlation = find_image_correlation(images)
print('Corner ids multiplied:', correlation[0][0] * correlation[-1][0] * correlation[-1][-1] * correlation[0][-1])


# Create merged images, stripping borders

for image in images.values() :
    image.trim()
combined_image = create_combined_image(correlation, images)

monster = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   '
]

sea_monsters = find_sea_monsters(combined_image, monster)

print('Number not in sea monsters:', sum([1 if x == '#' else 0 for row in combined_image.data for x in row]))

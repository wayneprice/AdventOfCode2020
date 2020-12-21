import math
import copy


class Image :
    def __init__(self, index, image_data) :
        self.__index = index
        self.__data = image_data
        self.__set_edges()

    def __set_edges(self) :
        self.__leftIndex = ''.join([ x[0] for x in self.__data ])
        self.__rightIndex = ''.join([ x[-1] for x in self.__data ])
        self.__topIndex = ''.join(self.__data[0])
        self.__bottomIndex = ''.join(self.__data[-1])

    def rotateCW(self):
        data = []
        for row in range(0, len(self.__data)) :
            data.append([])
            for col in range(0, len(self.__data)) :
                data[row].append(self.__data[len(self.__data)-col-1][row])
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
        for row in self.__data :
            print(''.join(row))
        print(self.__leftIndex, self.__topIndex, self.__rightIndex, self.__bottomIndex)
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
                image_row = [ c for c in image_row.rstrip() ]
                if not image_row :
                    break
                image_data.append(image_row)

            images[tile_index] = Image(tile_index, image_data)

    return images


def find_image_correlation(images) :
    images = copy.deepcopy(images)

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
    result = [[ None for i in range(0, result_size)] for j in range(0, result_size)]

    # Start with a corner image for the top-left, and orient it correctly
    top_left = next(index for index, edges in image_edges.items() if edges == 2)
    top_left_image = images[top_left]
    while edge_frequency[top_left_image.left_index] != 1 or edge_frequency[top_left_image.top_index] != 1 :
        top_left_image.rotateCW()
    result[0][0] = top_left_image
    del images[top_left]

    # Complete the top row
    for col in range(1, result_size) :
        prev_image = result[0][col-1]
        for index, image in images.items() :
            if prev_image.right_index in image.edge_indexes :
                while prev_image.right_index not in [ image.left_index, image.left_index[::-1]] :
                    image.rotateCW()
                if prev_image.right_index != image.left_index :
                    image.flipVertical()
                result[0][col] = image
                del images[index]
                break

    # Complete the remaining rows using the row above
    for row in range(1, result_size) :
        for col in range(0, result_size) :
            top_image = result[row-1][col]
            for index, image in images.items():
                if top_image.bottom_index in image.edge_indexes :
                    while top_image.bottom_index not in [ image.top_index, image.top_index[::-1]] :
                        image.rotateCW()
                    if top_image.bottom_index != image.top_index :
                        image.flipHorizontal()
                    result[row][col] = image
                    del images[index]
                    break

    return result


def create_combined_image(correlation) :
    image_size = correlation[0][0].size - 2
    data = []
    for row in range(0, len(correlation)) :
        for y in range(0, image_size) :
            rowdata = []
            for image in correlation[row] :
                rowdata.extend(image.data[y+1][1:-1])
            data.append(rowdata)
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
                            for sx in range(len(sea_monster[0])):
                                if sea_monster[sy][sx] == '#':
                                    combined_image.data[y+sy][x+sx] = 'O'
                        sea_monsters.append((x, y))

            combined_image.rotateCW()
        combined_image.flipVertical()

    return sea_monsters


# Read images
images = read_images('data/input-day20.txt')

# Match images
correlation = find_image_correlation(images)
print('Corner ids multiplied:', correlation[0][0].index * correlation[-1][0].index * correlation[-1][-1].index * correlation[0][-1].index)

# Create merged images, stripping borders
combined_image = create_combined_image(correlation)

# Search for sea monsters; modifies combined image
monster = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   '
]
sea_monsters = find_sea_monsters(combined_image, monster)

print('Number not in sea monsters:', sum([1 if x == '#' else 0 for row in combined_image.data for x in row]))

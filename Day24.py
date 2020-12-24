import re


directions = { 'ne': (1, 1), 'nw': (-1, 1), 'se': (1, -1), 'sw': (-1, -1), 'e': (2, 0), 'w': (-2, 0) }


def initialise_tiles(instructions) :
    global directions

    tiles = []
    for instruction in instructions :
        tile_location = [ 0, 0 ]
        for path in instruction :
            tile_location[0] += directions[path][0]
            tile_location[1] += directions[path][1]
        tile_location = tuple(tile_location)
        if tile_location in tiles :
            tiles.remove(tile_location)
        else :
            tiles.append(tile_location)

    return tiles

def flip_tiles(tiles) :
    global directions

    tiles_to_check = set(tiles)
    for black_tile in tiles :
        tiles_to_check.update(set([ tuple([black_tile[0] + direction[0], black_tile[1] + direction[1]]) for direction in directions.values()]
))

    new_tiles = []
    for tile in tiles_to_check :
        neighbour_count = sum([1 if tuple([tile[0] + direction[0], tile[1] + direction[1]]) in tiles else 0 for direction in directions.values()])
        if tile in tiles :  # Black tile
            if neighbour_count in [ 1, 2 ] :
                new_tiles.append(tile)
        else :
            if neighbour_count == 2 :
                new_tiles.append(tile)

    return new_tiles


with open('data/input-day24.txt', 'r') as fp :
    instructions = [ re.findall('(ne|nw|se|sw|e|w)', line.strip()) for line in fp ]

tiles = initialise_tiles(instructions)
print('Black tiles: ', len(tiles))

for turn in range(1, 101) :
    tiles = flip_tiles(tiles)
    print('Turn {}: Black tiles: {}'.format(turn, len(tiles)))


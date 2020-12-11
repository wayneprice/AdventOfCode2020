

with open('data/input-day3.txt' , 'r') as f:
    lines = f.readlines()
tree_map = [line.strip() for line in lines]


def count_trees(tree_map, route, origin = (0, 0)) :
    tree_count = 0

    x, y = origin
    while y < len(lines) :
        if tree_map[y][x % len(tree_map[y])] == '#' :
            tree_count += 1

        x += route[0]
        y += route[1]

    return tree_count


print(count_trees(tree_map, (3, 1)))

result = 1
for route in ( (1, 1), (3, 1), (5, 1), (7, 1), (1, 2) ) :
    result *= count_trees(tree_map, route)
print(result)


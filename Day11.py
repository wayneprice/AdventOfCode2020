

# When reading the file, surround the data with 'X' to make processing easier

def load_seating() :
    with open('data/input-day11.txt', 'r') as fp:
        seating = [ 'X' + x.strip() + 'X' for x in fp.readlines() ]
    seating.insert(0, 'X'*len(seating[0]))
    seating.append('X'*len(seating[0]))
    return list(map(list, seating))


def allocate_seating1(seating) :

    adjacency = ( (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1) )

    new_seating = [x[:] for x in seating]
    while True :
        changed = False
        for r in range(1, len(seating)-1) :
            for c in range(1, len(seating[r])-1) :
                current_seat = seating[r][c]
                if current_seat == '.' :
                    continue

                occupied = 0
                for offset in adjacency :
                    occupied += 1 if seating[r+offset[0]][c+offset[1]] == '#' else 0

                if current_seat == 'L' and occupied == 0 :
                    changed = True
                    new_seating[r][c] = '#'
                if current_seat == '#' and occupied >= 4 :
                    changed = True
                    new_seating[r][c] = 'L'

        if not changed :
            break

        seating = [x[:] for x in new_seating]

    return sum([ x.count('#') for x in seating ])


def allocate_seating2(seating) :
    while True :
        new_seating = [x[:] for x in seating]

        changed = False
        adjacency = ( (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1) )
        for r in range(1, len(seating)-1) :
            for c in range(1, len(seating[r])-1) :
                current_seat = seating[r][c]
                if current_seat == '.' :
                    continue

                occupied = 0
                for direction in adjacency :
                    offset = direction
                    while True :
                        seat = seating[r+offset[0]][c+offset[1]]
                        if seat == '#' :
                            occupied += 1
                        if seat != '.' :
                            break
                        offset = (offset[0] + direction[0], offset[1] + direction[1])

                if current_seat == 'L' and occupied == 0 :
                    changed = True
                    new_seating[r][c] = '#'
                if current_seat == '#' and occupied >= 5 :
                    changed = True
                    new_seating[r][c] = 'L'

        if not changed :
            break

        seating = [x[:] for x in new_seating]


    return sum([ x.count('#') for x in seating ])


seating = load_seating()
print(allocate_seating1(seating))
print(allocate_seating2(seating))


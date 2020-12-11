
max_seat_id = 0

seats = []

with open('data/input-day5.txt' , 'r') as fp:
    for line in fp :
        row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
        seat = int(line[7:].replace('L', '0').replace('R', '1'), 2)
        seat_id = row*8 + seat
        seats.append(seat_id)

min_seat_id = min(seats)
max_seat_id = max(seats)   


print(max_seat_id)
missing_seats = list(set(range(min_seat_id, max_seat_id+1)).difference(seats))
print(missing_seats[0])


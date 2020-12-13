
with open('data/input-day13.txt', 'r') as fp:
    earliest_timestamp = int(fp.readline().strip())
    all_buses = [x for x in fp.readline().strip().split(',')]

in_service_buses = [ (index, int(bus)) for index, bus in enumerate(all_buses) if bus != 'x']


bus_delays = { bus: bus - earliest_timestamp % bus for _, bus in in_service_buses }
least_delay = min(bus_delays.values())
first_bus = next((bus for bus, delay in bus_delays.items() if delay == least_delay))
print(first_bus * least_delay)


current_time, increment = 0, 1
for index, bus in in_service_buses :
    while (index + current_time) % bus != 0 :
        current_time += increment
    increment *= bus

print(current_time)



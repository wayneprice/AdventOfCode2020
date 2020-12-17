import collections
import functools



def read_data_file() :
    with open('data/input-day16.txt', 'r') as fp :
        rules = read_ticket_rules(fp)

        # Skip 'your ticket' comment
        fp.readline()
        my_ticket = read_tickets(fp)[0]

        fp.readline()
        other_tickets = read_tickets(fp)

        return rules, my_ticket, other_tickets

def read_ticket_rules(fp) :
    rules = {}
    while True :
        line = fp.readline().strip()
        if not line :
            break
        field, data = line.split(': ')
        ranges = [tuple(map(int, x.split('-'))) for x in data.split(' or ') ]
        rules[field] = ranges

    return rules

def read_tickets(fp) :
    tickets = []
    while True :
        line = fp.readline().strip()
        if not line :
            break
        tickets.append(tuple(map(int, line.split(','))))
    return tickets


def scanning_error_rate(rules, tickets) :
    combined_rules = [ range for ranges in rules.values() for range in ranges ]
    error_rate = 0
    invalid_tickets = []
    for ticket in tickets :
        for field in ticket :
            if not [x for x in combined_rules if x[0] <= field <= x[1]] :
                error_rate += field
                invalid_tickets.append(ticket)
        pass
    return error_rate, invalid_tickets


def find_field_indexes(rules, all_tickets) :
    field_indexes = collections.defaultdict(list)
    for idx, field_values in enumerate(list(map(tuple, zip(*all_tickets)))) :
        for rule_name, rule_ranges in rules.items() :
            if all([any([x[0] <= value <= x[1] for x in rule_ranges]) for value in field_values]) :
                field_indexes[rule_name].append(idx)

    unique_indexes = {}
    while field_indexes :
        field, value = next((k, v[0]) for k, v in field_indexes.items() if len(v) == 1 )
        unique_indexes[field] = value
        field_indexes.pop(field)
        for field in field_indexes.keys() :
            field_indexes[field].remove(value)

    return unique_indexes



rules, my_ticket, other_tickets = read_data_file()

error_rate, invalid_tickets = scanning_error_rate(rules, other_tickets)
print('Error rate:', error_rate)

valid_tickets = [ ticket for ticket in other_tickets if ticket not in invalid_tickets ]
field_indexes = find_field_indexes(rules, valid_tickets)
print('Product:', functools.reduce(lambda x, y : x*y, [my_ticket[idx] for field, idx in field_indexes.items() if field[:9] == 'departure']))

import re


hcl_re = re.compile('#[0-9a-f]{6}')
pid_re = re.compile('[0-9]{9}')


def simple_valid(data) :
    required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
    if len(required_fields.intersection(data.keys())) < len(required_fields) :
        return False

    return True


def full_valid(data) :
    required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
    if len(required_fields.intersection(data.keys())) < len(required_fields) :
        return False

    byr = int(data['byr'])
    if byr < 1920 or byr > 2002 :
        return False

    iyr = int(data['iyr'])
    if iyr < 2010 or iyr > 2020 :
        return False

    eyr = int(data['eyr'])
    if eyr < 2020 or eyr > 2030 :
        return False

    if data['hgt'].endswith('cm') :
        hgt = int(data['hgt'][:-2])
        if hgt < 150 or hgt > 193 :
            return False
    elif data['hgt'].endswith('in') :
        hgt = int(data['hgt'][:-2])
        if hgt < 59 or hgt > 76 :
            return False
    else :
        return False

    if not hcl_re.fullmatch(data['hcl']) :
        return False

    if data['ecl'] not in [ 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' ] :
        return False

    if not pid_re.fullmatch(data['pid']) :
        return False

    return True


def read_data(filename) :
    with open(filename , 'r') as fp:

        data = []
        fields = {}
        for line in fp :
            line = line.strip()

            if not line :
                data.append(fields)
                fields = {}
                continue

            for kv in line.split(' ') :
                key, value = kv.split(':')
                fields[key] = value

        if fields :
            data.append(fields)

    return data



data = read_data('data/input-day4.txt')

simple_count = 0
full_count = 0
for fields in data :
    simple_count += simple_valid(fields)
    full_count += full_valid(fields)


print(simple_count)
print(full_count)


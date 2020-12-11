
import re


with open('data/input-day2.txt', 'r') as f:
    data = f.readlines()


def process_rules(data) :
    pattern = r'([0-9]+)-([0-9]+) (.): (.+)'
    rules = []
    for item in data :
        m = re.fullmatch(pattern, item.strip())
        if not m :
            raise RuntimeError('Failed to process rule')

        rules.append((int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)))

    return rules


def validate_part1(rules) :
    valid_count = 0
    for min, max, letter, value in rules :

        count = {}
        for c in value:
            count[c] = count[c] + 1 if c in count else 1

        c = count[letter] if letter in count else 0
        if c >= min and c <= max :
            valid_count += 1

    return valid_count


def validate_part2(rules) :
    valid_count = 0
    for min, max, letter, value in rules :

        first = value[min-1] == letter
        second = value[max-1] == letter
        if (first or second) and not (first and second) :
            valid_count += 1

    return valid_count


rules = process_rules(data)
print(validate_part1(rules))
print(validate_part2(rules))


import collections


def read_data() :
    rules = collections.defaultdict(dict)

    with open('data/input-day7.txt' , 'r') as fp:

        for line in fp :
            parent, children = line.strip()[:-1].split(' contain ')
            parent = parent.rstrip('s')[:-4]
            for child in children.split(',') :
                child = child.strip().rstrip('s')[:-4]
                if child == 'no other' :
                    continue
                num, desc = child.split(' ', 1)
                rules[parent].update({desc: int(num)})

    return rules


rules = read_data()

search_bag = 'shiny gold'

contains_bag = set()
search = set([search_bag])
while search :
    current = search.pop()
    for k, v in rules.items() :
        if current in v :
            search.add(k)
            contains_bag.add(k)

print(len(contains_bag))


def count_bags(bag) :
    count = 1
    if bag in rules :
        for child_bag, num in rules[bag].items() :
            count += num * count_bags(child_bag)

    return count

print(count_bags('shiny gold')-1)


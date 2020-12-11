

sum_anyone = 0
sum_everyone = 0


group_answers = []
with open('data/input-day6.txt' , 'r') as fp:

    answers = []
    for line in fp :
        line = line.strip()

        if not line :
            group_answers.append(answers)
            answers = []
            continue

        answers.append([c for c in line])

    if answers :
        group_answers.append(answers)


sum_anyone = 0
sum_everyone = 0

for group in group_answers :
    all_answers = set([item for sublist in group for item in sublist])
    sum_anyone += len(all_answers)

    common_answers = set.intersection(*map(set, group))
    sum_everyone += len(common_answers)

print(sum_anyone)
print(sum_everyone)



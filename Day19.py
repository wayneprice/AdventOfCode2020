import collections


def read_input(filename) :
    with open(filename, 'r') as fp :
        grammar = collections.defaultdict(list)
        for line in fp :
            line = line.rstrip()
            if not line :
                break
            id, rules = line.split(':', 1)
            for rule in rules.split('|') :
                rule = [ int(x) if x.isdigit() else x.strip('"') for x in rule.split() ]
                grammar[int(id)].append(rule)

        data = []
        for line in fp :
            data.append(line.rstrip())

    return grammar, data


class MessageParser :
    def __init__(self, grammar) :
        self.__grammar = grammar

    def validate_message(self, message) :
        remaining = self.process_rule(message)
        return len(list(filter(lambda x: len(x) == 0, remaining))) > 0

    def process_rule(self, message, rule = 0) :
        results = []
        for rules in self.__grammar[rule] :
            remaining = [ message ]
            for x in rules :
                result = []
                for str in remaining:
                    if isinstance(x, int) :
                        result.extend(self.process_rule(str, x))
                    else :
                        if str and str[0] == x :
                            str = str[1:]
                            result.append(str)
                remaining = result
            results.extend(remaining)
        return results


grammar, messages = read_input('data/input-day19.txt')

parser = MessageParser(grammar)
count = sum([parser.validate_message(message) for message in messages])
print(count)

grammar[8] = [[42], [42, 8]]
grammar[11] = [[42, 31], [42, 11, 31]]

parser = MessageParser(grammar)
count = sum([parser.validate_message(message) for message in messages])
print(count)

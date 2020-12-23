

class Node :
    def __init__(self, value) :
        self.value = value
        self.next = None


class CrabsGame :
    def __init__(self, values):
        self.__min_value = min(values)
        self.__max_value = max(values)
        self.__nodes = { value: Node(value) for value in values }
        for idx, value in enumerate(values) :
            self.__nodes[value].next = self.__nodes[values[(idx+1) % len(values)]]
        self.current = self.__nodes[values[0]]

    def play_turn(self):
        removed_head = self.current.next
        removed_tail = removed_head.next.next
        removed_values = [ removed_head.value, removed_head.next.value, removed_tail.value ]
        self.current.next = removed_tail.next

        destination_value = self.current.value
        while True :
            destination_value -= 1
            if destination_value < self.__min_value :
                destination_value = self.__max_value
            if destination_value not in removed_values :
                break

        destination_node = self.__nodes[destination_value]
        removed_tail.next = destination_node.next
        destination_node.next = removed_head

        self.current = self.current.next

    def node(self, value) :
        return self.__nodes[value]




input = '538914762'

# Part 1

cups = [ int(x) for x in input]

game = CrabsGame(cups)
for turn in range(0, 100) :
    game.play_turn()

node = game.node(1).next
result = []
while node.value != 1 :
    result.append(node.value)
    node = node.next
print('Part 1:', ''.join(map(str, result)))


# Part 2

cups = [ int(x) for x in input ]
cups.extend(range(max(cups)+1, 1000001))
game = CrabsGame(cups)
for turn in range(0, 10000000) :
    game.play_turn()

node = game.node(1)
print('Part 2:', node.next.value * node.next.next.value)

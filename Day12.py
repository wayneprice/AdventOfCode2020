

class Ferry :
    def __init__(self, initial_pos = (0, 0), motionMethod = None) :
        self.__motionMethod = motionMethod
        self.__x = initial_pos[0]
        self.__y = initial_pos[1]

    def move(self, action, value) :
        offset = self.__motionMethod.move(action, value)
        self.__x += offset[0]
        self.__y += offset[1]

    @property
    def x(self) :
        return self.__x

    @property
    def y(self) :
        return self.__y


class NoWaypointMethod :
    __moveActions = { 'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0) }
    __dirActions = { 0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1) }

    def __init__(self) :
        self.__direction = 0

    def move(self, action, value) :
        if action in self.__moveActions :
            return (self.__moveActions[action][0] * value, self.__moveActions[action][1] * value)
        elif action == 'L' :
            self.__direction = (self.__direction + value) % 360
            return (0, 0)
        elif action == 'R' :
            self.__direction = (self.__direction + 360 - value) % 360
            return (0, 0)
        elif action == 'F' :
            return (self.__dirActions[self.__direction][0] * value, self.__dirActions[self.__direction][1] * value)
        else:
            raise RuntimeError('Invalid action {}'.format(action))


class WaypointMethod :
    __moveActions = { 'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0) }

    def __init__(self, initial) :
        self.__x = initial[0]
        self.__y = initial[1]

    def move(self, action, value) :
        if action in self.__moveActions :
            self.__x += self.__moveActions[action][0] * value
            self.__y += self.__moveActions[action][1] * value
            return (0, 0)
        elif action == 'L':
            if value == 90 :
                self.__x, self.__y = -self.__y, self.__x
            elif value == 180 :
                self.__x, self.__y = -self.__x, -self.__y
            elif value == 270 :
                self.__x, self.__y = self.__y, -self.__x
            return (0, 0)
        elif action == 'R':
            return self.move('L', 360-value)
        elif action == 'F' :
            return (self.__x * value, self.__y * value)


# When reading the file, surround the data with 'X' to make processing easier

def load_actions() :
    with open('data/input-day12.txt', 'r') as fp:
        actions = [ (x[0], int(x[1:])) for x in fp.readlines()]
    return actions



actions = load_actions()

ferry = Ferry(motionMethod = NoWaypointMethod())
for action in actions :
    ferry.move(action[0], action[1])

print('Final Pos: {}  Distance: {}'.format((ferry.x, ferry.y), abs(ferry.x)+abs(ferry.y)))


ferry = Ferry(motionMethod = WaypointMethod(initial = (10, 1)))
for action in actions :
    ferry.move(action[0], action[1])

print('Final Pos: {}  Distance: {}'.format((ferry.x, ferry.y), abs(ferry.x)+abs(ferry.y)))

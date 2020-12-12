

class Ferry :
    def __init__(self) :
        self.__x = 0
        self.__y = 0
        self.__direction = 0    # 0 = E, 90 = N, 180 = W, 270 = S
        self.__directionOffset = { 0 : (1, 0), 90 : (0, 1), 180 : (-1, 0), 270 : (0, -1) }

    def move(self, action, value) :
        if action == 'N' :
            self.__y += value
        elif action == 'S' :
            self.__y -= value
        elif action == 'E' :
            self.__x += value
        elif action == 'W' :
            self.__x -= value
        elif action == 'L' :
            self.__direction = (self.__direction + value) % 360
        elif action == 'R' :
            self.__direction = (self.__direction - value + 360) % 360
        elif action == 'F' :
            self.__x += value * self.__directionOffset[self.__direction][0]
            self.__y += value * self.__directionOffset[self.__direction][1]
        else:
            raise RuntimeError('Invalid action {}'.format(action))

    @property
    def x(self) :
        return self.__x

    @property
    def y(self) :
        return self.__y


class Waypoint :
    def __init__(self, ferry, init_x, init_y) :
        self.__ferry = ferry
        self.__x = init_x
        self.__y = init_y

    def move(self, action, value) :
        if action == 'N':
            self.__y += value
        elif action == 'S':
            self.__y -= value
        elif action == 'E':
            self.__x += value
        elif action == 'W':
            self.__x -= value
        elif action == 'L':
            if value == 90 :
                self.__x, self.__y = -self.__y, self.__x
            elif value == 180 :
                self.__x, self.__y = -self.__x, -self.__y
            elif value == 270 :
                self.__x, self.__y = self.__y, -self.__x
        elif action == 'R':
            self.move('L', 360-value)
        elif action == 'F' :
            self.__ferry.move('E', value * self.__x)
            self.__ferry.move('N', value * self.__y)


# When reading the file, surround the data with 'X' to make processing easier

def load_actions() :
    with open('data/input-day12.txt', 'r') as fp:
        actions = [ (x[0], int(x[1:])) for x in fp.readlines()]
    return actions



actions = load_actions()


ferry = Ferry()
for action in actions :
    ferry.move(action[0], action[1])

print(ferry.x, ferry.y, abs(ferry.x)+abs(ferry.y))


ferry = Ferry()
waypoint = Waypoint(ferry, 10, 1)
for action in actions :
    waypoint.move(action[0], action[1])

print(ferry.x, ferry.y, abs(ferry.x)+abs(ferry.y))

import random

WIDTH, HEIGHT = 500, 500
SIZE = 10
W, H = WIDTH//SIZE, HEIGHT//SIZE

BACKGROUNDCOLOR = '#303030'

TICK_TIME = 250

OBJECTS_QUANTITY = 64
AGENTS_QUANTITY = 64
BEST_ARR_LEN = 8

DIR_ARR = [[-1, -1],
           [0, -1],
           [1, -1],
           [1, 0],
           [1, 1],
           [0, 1],
           [-1, 1],
           [-1, 0],
           ]


FPS = 120

BRAIN_SIZE = 64

BG_COLOR = (50, 50, 50)
NET_COLOR = (80, 80, 80)
AGENT_COLOR = (50, 50, 150)
FOOD_COLOR = (50, 150, 50)
POISON_COLOR = (150, 50, 50)


class StandartObj:
    def __init__(self, x=-1, y=-1, arr=[]):
        if x == -1:
            self.x, self.y = create_random_pos(arr)
        else:
            self.x, self.y = x, y

class Wall(StandartObj):
    pass

class Poison(StandartObj):
    pass

class Food(StandartObj):
    pass

class Collision:
    def __init__(self, is_collision, col_type=None, obj=None):
        self.is_collision = is_collision
        self.col_type = col_type
        self.col_obj = obj


def create_random_pos(arr):
    while True:
        x, y = random.randint(1, W-1), random.randint(1, H-1)
        collision = check_allow_pos(x, y, arr)
        if not collision.is_collision: return x, y

def check_allow_pos(x, y, arr):
    for i in arr:
        if i.x == x and i.y == y:
            return Collision(True, type(i), obj=i)
    return Collision(False)


def mutate(arr):
    # new_arr = []
    # for point in arr:
    #     if random.random() < 0.1:
    #         new_arr.append()
    #     else:
    #         new_arr.append(point)

    for i in range(random.randint(8, 16)):
        if random.random() < 0.5:
            arr[random.randint(0, BRAIN_SIZE-1)] = random.randint(0, BRAIN_SIZE-1)

    return arr


class Agent:
    def __init__(self, arr, brain=[], unmut=0):
        self.x, self.y = create_random_pos(arr)
        self.brain = brain if len(brain) > 0 else [random.randint(0, 24) for _ in range(BRAIN_SIZE)] #[24, 10, 37, 42, 57, 13, 24, 45, 17, 18, 37, 57, 55, 29, 36, 46, 12, 56, 37, 46, 12, 29, 7, 21, 41, 32, 19, 23, 20, 28, 38, 35, 20, 55, 63, 26, 49, 41, 44, 53, 50, 13, 42, 29, 0, 60, 35, 8, 35, 51, 17, 17, 17, 54, 20, 27, 55, 20, 44, 62, 44, 4, 30, 32]
        self.point = 0
        self.hp = 25
        self.live_len = 0
        self.unmut = unmut
        self.direction = 0

    def update(self, objects, counter = 0):
        if counter >= 20:
            self.hp -= 2
            return

        command = self.brain[self.point]
        if command < 8:
            x = self.x + DIR_ARR[(command + self.direction) % 8][0]
            y = self.y + DIR_ARR[(command + self.direction) % 8][1]
            collision = check_allow_pos(x, y, objects)
            if not collision.is_collision:
                self.x, self.y = x, y
            if collision.col_type in [Poison, Wall]:
                self.hp = 0
                self.live_len //= 3

            self.point = (self.point + 1) % BRAIN_SIZE
            self.hp -= 1


        elif command < 16:
            self.direction = ((command + self.direction) % 8)
            self.point = (self.point + 1) % BRAIN_SIZE
            self.update(objects, counter + 1)



        elif command < 24:
            x = self.x + DIR_ARR[(command + self.direction) % 8][0]
            y = self.y + DIR_ARR[(command + self.direction) % 8][1]
            collision = check_allow_pos(x, y, objects)
            if collision.is_collision:
                if collision.col_type == Food:
                    self.hp += 50
                    objects.remove(collision.col_obj)
                    objects.append(Food(arr=objects) if random.randint(1,2) == 1 else Poison(arr=objects))


                elif collision.col_type == Poison:
                    x, y = collision.col_obj.x, collision.col_obj.y
                    objects.remove(collision.col_obj)
                    objects.append(Food(x, y))

            self.hp -= 1
            self.point = (self.point + 1) % BRAIN_SIZE



        elif command < 32:
            x = self.x + DIR_ARR[(command + self.direction) % 8][0]
            y = self.y + DIR_ARR[(command + self.direction) % 8][1]
            collision = check_allow_pos(x, y, objects)
            if collision.is_collision:
                delta = [Food, Poison, Agent, Wall].index(collision.col_type) + 2
                self.point = (self.point + delta) % BRAIN_SIZE
            else:
                self.point = (self.point + 1) % BRAIN_SIZE

            self.update(objects, counter + 1)


        else:
            self.point = (self.point + command) % BRAIN_SIZE
            self.update(objects, counter+1)

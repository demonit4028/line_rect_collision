import numpy as np
import pygame
import random
import copy
from pygame_lib_v1 import *


def relu(x):
    return (x>0)*x

class Net:
    def __init__(self):
        self.input_layer = 16 + 1
        self.hidden_layer = 30
        self.output_layer = 8


        self.weight_01 = 2 * np.random.random((self.input_layer, self.hidden_layer)) - 1
        self.weight_12 = 2 * np.random.random((self.hidden_layer, self.output_layer)) - 1

    def forward(self, input_layer):
        hidden_layer = relu(np.dot(input_layer, self.weight_01))
        output_layer = np.dot(hidden_layer, self.weight_12)
        return output_layer


def biggest(arr):
    max = -500
    ind = 0
    for i in range(np.shape(arr)[0]):
        if arr[i] > max:
            max = arr[i]
            ind = i
    return ind

def is_sth_there(pos):
    for i in bots_arr:
        if pos[0] == i.pos[0] and pos[1] == i.pos[1]:
            return True
    return False


def touching(pos, arr):
    for i in arr:
        if pos[0] == i[0] and pos[1] == i[1]:
            return True
    return False


def find_best_hp():
    hp = 0
    ind = 0
    for i in range(len(bots_arr)):
        if bots_arr[i].hp > hp:
            hp = bots_arr[i].hp
            ind = i

    return ind

def find_best_formula(arr):
    num = 0
    ind = 0
    for i in range(len(arr)):
        a = arr[i].points # life_len * arr[i].life_len * 2**min(arr[i].eaten_food, 10) * max(1, arr[i].eaten_food-9)
        if a > num:
            num = a
            ind = i
    return arr[ind]



def sort_bests():
    yyy = sorted(bests_bots, key=lambda x: x.points)
    return copy.deepcopy(yyy)

def find_mother_father():
    bests_bots = sort_bests()

    arr = []
    sum = 0
    for i in bests_bots:
        sum += i.points
        arr.append(i.points)



    for i in range(len(arr)):
        arr[i] = arr[i] / sum


    arr.append(sum)

    a = random.random()
    father = 0
    for i in range(len(arr) - 1):
        if arr[i] < a < arr[i + 1]:
            father = i
            # print(a, i)

    a = random.random()
    mother = 0
    for i in range(len(arr) - 1):
        if arr[i] < a < arr[i + 1]:
            mother = i


    # print(father, mother)
    return bests_bots[father], bests_bots[mother]


def crossing():
    new_bots = []
    for i in range(len(bests_bots)):
        new_bots.append(Bot())
        f, m = find_mother_father()


        for y in range(np.shape(new_bots[i].brain.weight_01)[0]):
            for x in range(np.shape(new_bots[i].brain.weight_01)[1]):
                if random.random() < 0.5:
                    new_bots[i].brain.weight_01[y, x] = f.brain.weight_01[y, x]
                else:
                    new_bots[i].brain.weight_01[y, x] = m.brain.weight_01[y, x]

        for y in range(np.shape(new_bots[i].brain.weight_12)[0]):
            for x in range(np.shape(new_bots[i].brain.weight_12)[1]):
                if random.random() < 0.5:
                    new_bots[i].brain.weight_12[y, x] = f.brain.weight_12[y, x]
                else:
                    new_bots[i].brain.weight_12[y, x] = m.brain.weight_12[y, x]

    return new_bots



def formula(x, y):
    return x * x * 2**y



def print_gens(bot):
    for y in range(np.shape(bot.brain.weight_01)[0]):
        print(bot.brain.weight_01[y])
    print("~"*100)
    for y in range(np.shape(bot.brain.weight_12)[0]):
        print(bot.brain.weight_12[y])

    print("/" * 100)


class Bot:
    def __init__(self):
        self.pos = np.array([random.randint(1, max_world_x-2), random.randint(1, max_world_y-2)])
        self.brain = Net()
        self.view = 20
        self.dead = False
        self.hp = 100
        self.life_len = 0
        self.eaten_food = 0
        self.food = [random.randint(1, max_world_x-2), random.randint(1, max_world_y-2)]
        self.points = formula(self.life_len, self.eaten_food)


    def draw(self):
        pygame.draw.rect(wnd, (0, 200, 200), (self.pos[0] * scale, self.pos[1] * scale, scale, scale))
        pygame.draw.rect(wnd, (200, 200, 0), (self.food[0] * scale, self.food[1] * scale, scale, scale))


    def mutation(self):
        for y in range(np.shape(self.brain.weight_01)[0]):
            for x in range(np.shape(self.brain.weight_01)[1]):
                if random.random() < 0.02:
                    self.brain.weight_01[y, x] = 2*random.random()-1

        for y in range(np.shape(self.brain.weight_12)[0]):
            for x in range(np.shape(self.brain.weight_12)[1]):
                if random.random() < 0.02:
                    self.brain.weight_12[y, x] = 2*random.random()-1


    def step(self):
        self.life_len += 1
        self.hp -= 1
        if self.hp <= 0:
            self.dead = True

        input_arr = np.zeros((17))
        iter = 0
        x, y = self.pos[0], self.pos[1]



        costil = False
        # food
        for dir in direction:
            for i in range(1, self.view):
                a = [x, y] + dir * i
                if a[0] == self.food[0] and a[1] == self.food[1]:
                    input_arr[iter] = i
                    costil = True
                    break

            if costil: break

            iter += 1

        # walls
        for dir in direction:
            for i in range(1, self.view):
                a = [x, y] + dir * i
                if touching(a, walls_arr):
                    # print(a, i, [x, y], dir)
                    input_arr[iter] = i # (dir[0] * i + dir[1] * i)
                    break

            iter += 1

        # print(input_arr)

        # смещение
        input_arr[iter] = 1

        move = self.brain.forward(input_arr)
        move = biggest(move)
        if touching(self.pos + direction[move], walls_arr):
            self.dead = True
        else:
            self.pos += direction[move]


        if self.pos[0] == self.food[0] and self.pos[1] == self.food[1]:
            self.hp += 100
            self.eaten_food += 1
            self.food = [random.randint(1, max_world_x-2), random.randint(1, max_world_y-2)]

        self.points = formula(self.life_len, self.eaten_food)

def UI_draw():
    textsurface = ui_myfont.render("Best hp - " + str(bots_arr[find_best_hp()].hp), False, (255, 255, 255))
    wnd.blit(textsurface, ((max_world_x+1)*scale, 0))

    textsurface = ui_myfont.render("Ep - " + str(ep), False, (255, 255, 255))
    wnd.blit(textsurface, ((max_world_x + 1) * scale, 20))

    textsurface = ui_myfont.render("Best l_time - " + str(best_living_time), False, (255, 255, 255))
    wnd.blit(textsurface, ((max_world_x + 1) * scale, 40))

    textsurface = ui_myfont.render("L_time - " + str(living_time), False, (255, 255, 255))
    wnd.blit(textsurface, ((max_world_x + 1) * scale, 60))

    textsurface = ui_myfont.render("Points_best - " + str(find_best_formula(bots_arr).points), False, (255, 255, 255))
    wnd.blit(textsurface, ((max_world_x + 1) * scale, 80))



max_world_x = 20
max_world_y = 20
scale = 20
bots = 50
drawing_flag = True
direction = np.array([
    [-1, -1],
    [0, -1],
    [1, -1],
    [-1, 0],
    [1, 0],
    [-1, 1],
    [0, 1],
    [1, 1]
])


bots_arr = [Bot() for i in range(bots)]
bests_bots = []

walls_arr = np.array([[0, 0] for i in range(max_world_x*2 + max_world_y*2)])
iter = 0
for x in range(max_world_x+1):
    walls_arr[iter] = [x, 0]
    iter += 1
    walls_arr[iter] = [x, max_world_y]
    iter += 1


for y in range(1, max_world_y):
    walls_arr[iter] = [0, y]
    iter += 1
    walls_arr[iter] = [max_world_x, y]
    iter += 1



WIDTH = 1000
HEIGHT = 550
wnd = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('v1.0')
clock = pygame.time.Clock()
FPS = 0
pygame.font.init()
ui_myfont = pygame.font.SysFont('Comic Sans MS', 20)

ui = UI()
ui.buttons.append(Button(WIDTH-200, HEIGHT-50, 200, 50, (0, 200, 0), (0, 150, 0), (0, 50, 0), (255, 255, 255),
                         "Write best gens"))
ui.buttons.append(Button(WIDTH-200, HEIGHT-100, 200, 50, (0, 200, 0), (0, 150, 0), (0, 50, 0), (255, 255, 255),
                         "Drawing"))


best_living_time = living_time = 0
ep = 0
while True:
    ep+=1

    if living_time > best_living_time:
        best_living_time = living_time
    living_time = 0

    bests_bots = []
    # print(len(bots_arr))
    # food_arr = [[random.randint(0, max_world_x), random.randint(0, max_world_x)] for i in range(food)]
    while len(bots_arr) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if drawing_flag:
            #         drawing_flag = False
            #     else:
            #         drawing_flag = True


        if ui.buttons[0].was_pressed():  # принт
            print_gens(find_best_formula(bots_arr))

        if ui.buttons[1].was_pressed():  # отрисовка
            drawing_flag = not drawing_flag






        ui.update()
        if drawing_flag:
            wnd.fill((20, 20, 20))
            UI_draw()
            ui.draw(wnd)

            for i in walls_arr:
                pygame.draw.rect(wnd, (200, 200, 200), (i[0] * scale, i[1] * scale, scale, scale))

            for bot in bots_arr:
                bot.draw()


        living_time += 1
        for bot in bots_arr:
            bot.step()



        next_bots = []
        for bot in bots_arr:
            if bot.dead == False:
                next_bots.append(bot)

            else:
                bests_bots.append(bot)


        bots_arr = copy.deepcopy(next_bots)

        pygame.display.update()
        clock.tick(FPS)



    bots_arr = copy.deepcopy(crossing())

    for i in range(int(bots * 0.6)):
        bots_arr[i].mutation()

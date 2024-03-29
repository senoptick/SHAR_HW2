import csv
import random
import numpy
from createMap import Map, create_csv
from pygame import Rect, display, QUIT, time, draw
from UI import Button, InputBox
import pygame
import sys

INPUT_BOXES = {}
BUTTONS = {}
COLORS = {"W": "water.jpg", "B": "bedrock.jpg",  "C": "cobble.jpg", "D": "dirt.jpg",
          "S": "sand.jpg", "G": "grass.jpg"}

BLACKLIST = ["W", "B"]


SIZE = temp_SIZE = (16, 16)
PIXEL = temp_PIXEL = 30
temp_ROBOT_POS = (0, 0)
create_csv(COLORS, SIZE)


class Robot:
    def __init__(self, coord=(0, 0)):
        self.surf = pygame.transform.scale(pygame.image.load('data/spider.png'), (PIXEL, PIXEL))
        self.rect = self.surf.get_rect(topleft=((coord[1] - 1) * PIXEL, (coord[0] - 1) * PIXEL))
        self.pos = coord
        self.hide = 256


    def update(self, sc):
        self.rect.x = self.pos[1] * PIXEL
        self.rect.y = self.pos[0] * PIXEL
        self.surf.set_alpha(self.hide)
        sc.blit(self.surf, self.rect)

    def visibility(self):
        self.hide = 256 - self.hide

    def move_up(self):
        self.pos = move_bot(self.pos, [0, 0, 1, 0])[0]

    def move_left(self):
        self.pos = move_bot(self.pos, [1, 0, 0, 0])[0]

    def move_right(self):
        self.pos = move_bot(self.pos, [0, 1, 0, 0])[0]

    def move_down(self):
        self.pos = move_bot(self.pos, [0, 0, 0, 1])[0]


def move_bot(robot_pos, direction, p_u=[0.15, 0.8, 0.05]): #left, right, up, down
    x, y = robot_pos
    n = random.randint(0, 100)
    dist = 0
    s = 0
    for i in range(len(p_u)):
        s += int(p_u[i]*100)
        if n <= s:
            dist = i
            break
    if dist == 0:
        return (x, y), 0
    else:
        if direction[0]: # лево
            if app.m.data[x, y - 1] not in BLACKLIST:
                if dist == 2:
                    if app.m.data[x, y - 2] not in BLACKLIST:
                        return (x, y - 2), 0
                    else:
                        return (x, y - 1), 1
                return (x, y - 1), 0
            else:
                return (x, y), 1

        elif direction[1]:  # право
            if app.m.data[x, y + 1] not in BLACKLIST:
                if dist == 2:
                    if app.m.data[x, y + 2] not in BLACKLIST:
                        return (x, y + 2), 0
                    else:
                        return (x, y + 1), 1
                return (x, y + 1), 0
            else:
                return (x, y), 1

        elif direction[2]:  # вверх
            if app.m.data[x-1, y] not in BLACKLIST:
                if dist == 2:
                    if app.m.data[x-2, y] not in BLACKLIST:
                        return (x-2, y), 0
                    else:
                        return (x-1, y), 1
                return (x-1, y), 0
            else:
                return (x, y), 1

        elif direction[3]:  # вниз
            if app.m.data[x+1, y] not in BLACKLIST:
                if dist == 2:
                    if app.m.data[x+2, y] not in BLACKLIST:
                        return (x+2, y), 0
                    else:
                        return (x+1, y), 1
                return (x+1, y), 0
            else:
                return (x, y), 1


def create_new_csv():
    create_csv(COLORS, (int(temp_SIZE), int(temp_SIZE)))


def load_new_csv():
    global SIZE, PIXEL, app, robot
    SIZE = (int(temp_SIZE), int(temp_SIZE))
    PIXEL = int(temp_PIXEL)
    robot = Robot()
    app = App()


def change_coord_bot():
    global robot
    robot.pos = temp_ROBOT_POS

def show_bot():
    robot.visibility()

def change_pos_bot(pos):
    global temp_ROBOT_POS
    temp_ROBOT_POS = tuple(map(int, pos.split()))


def change_size_map(size):
    global temp_SIZE
    temp_SIZE = size


def change_size_pixel(size):
    global temp_PIXEL
    temp_PIXEL = size


class Minimap:
    def __init__(self, PIXEL, SIZE):
        self.word_h = SIZE[0]
        self.word_w = SIZE[1]

    def draw_minimap(self):
        self.word_h = SIZE[0]
        self.word_w = SIZE[1]
        self.robot_minimap = Robot((self.word_h/2, self.word_w*2))
        env, local_robot_pos = local_map()
        for x in range(env.shape[0]):
            for y in range(env.shape[1]):
                block = env[x, y]
                if block != '0':
                    self.surf = pygame.transform.scale(pygame.image.load("data/" + COLORS[block]), (PIXEL, PIXEL))
                    self.rect = self.surf.get_rect(topleft=((y + self.word_w * 2 - 2)*PIXEL, (x + self.word_h / 2 - 2) * PIXEL))
                    app.sc.blit(self.surf, self.rect)
        app.sc.blit(self.robot_minimap.surf, self.robot_minimap.rect)


def local_map():
    m = app.m.data
    robot_pos = 1, 1
    return numpy.array([[0, m[robot.pos[0]-1, robot.pos[1]], 0],
                       [m[robot.pos[0], robot.pos[1]-1], m[robot.pos[0], robot.pos[1]], m[robot.pos[0], robot.pos[1]+1]],
                       [0, m[robot.pos[0]+1, robot.pos[1]], 0]]), robot_pos


class App:
    def __init__(self):
        global BUTTONS, INPUT_BOXES, robot
        self.m = Map(COLORS)



        self.coordinates = self.m.coordinates()
        self.h_map, self.w_map = self.m.shape(PIXEL)

        self.sc = display.set_mode((self.w_map * 2 + 200, self.h_map))
        self.sc.fill((255, 255, 255))

        while self.m.data[robot.pos] in BLACKLIST:
            robot.pos = random.randint(0, SIZE[0]), random.randint(0, SIZE[1])
            robot.hide = 0
            robot.update(self.sc)

        self.inp_pos_bot = InputBox(SIZE, PIXEL, str(robot.pos[0]) + ' ' + str(robot.pos[1]), 1)
        self.inp_size_map = InputBox(SIZE, PIXEL, str(SIZE[0]), 2)
        self.inp_size_pixel = InputBox(SIZE, PIXEL, str(PIXEL), 3)
        self.btn_move_bot = Button(SIZE, PIXEL, "Переместить робота        robot pos", 1)
        self.btn_create_csv = Button(SIZE, PIXEL, "Создать локацию           map size:", 2)
        self.btn_load_csv = Button(SIZE, PIXEL, "Загрузить локацию        pixel size:", 3)

        self.btn_show = Button(SIZE, PIXEL, "Показать/Скрыть бота", 4)

        BUTTONS = {self.btn_move_bot: change_coord_bot,
                   self.btn_create_csv: create_new_csv,
                   self.btn_load_csv: load_new_csv,
                   self.btn_show: show_bot}
        INPUT_BOXES = {self.inp_pos_bot: change_pos_bot,
                       self.inp_size_map: change_size_map,
                       self.inp_size_pixel: change_size_pixel}

    def update(self):
        for color in self.coordinates:
            self.surf = pygame.transform.scale(pygame.image.load("data/" + COLORS[color]), (PIXEL, PIXEL))
            for y, x in self.coordinates[color]:
                self.rect = self.surf.get_rect(topleft=(x * PIXEL, y * PIXEL))
                self.sc.blit(self.surf, self.rect)

        minimap.draw_minimap()
        robot.update(self.sc)

        app.create_UI()
        display.update()

    def create_UI(self):
        for inp in INPUT_BOXES:
            inp.draw(self.sc)
        for button in BUTTONS:
            button.drawing(self.sc)


if __name__ == "__main__":
    robot = Robot()
    minimap = Minimap(PIXEL, SIZE)
    app = App()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for btn in BUTTONS:
                    if btn.rect.collidepoint(event.pos):
                        BUTTONS[btn]()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    robot.move_right()
                    robot.update(app.sc)
                elif event.key == pygame.K_LEFT:
                    robot.move_left()
                    robot.update(app.sc)
                elif event.key == pygame.K_UP:
                    robot.move_up()
                    robot.update(app.sc)
                elif event.key == pygame.K_DOWN:
                    robot.move_down()
                    robot.update(app.sc)
            for box in INPUT_BOXES:
                box.handle_event(event)
                INPUT_BOXES[box](box.text)

        app.sc.fill((255, 255, 255))
        app.update()
        time.delay(100)

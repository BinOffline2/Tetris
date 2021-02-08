"""Der gesamte ursprüngliche code basiert auf TheMorpheus https://youtu.be/SfPWCKTHzE4"""
import pygame
import random

colors = [
    (0, 0, 0),
    (0, 240, 240),          # 4 in ein Reihe
    (0, 0, 240),            # Reverse L
    (240, 160, 0),          # L
    (240, 240, 0),          # Block
    (0, 240, 0),            # S
    (160, 0, 240),          # T
    (240, 0, 0),            # Reverse S
]

class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],                                  # Gerade
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],      # Reverse L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],    # L
        [[1, 2, 5, 6]],                                                 # Block
        [[6, 7, 9, 10], [1, 5, 6, 10]],                                 # S
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],       # T
        [[4, 5, 9, 10], [2, 6, 5, 9]]                                   # Reverse S
    ]

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.type = random.randint(0, len(self.figures)-1)
        self.color = colors[self.type+1]
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation+1) % len(self.figures[self.type])


class Tetris:
    height = 0
    width = 0
    field = []
    score = 0
    state = "start"
    figure = None

    def __init__(self, _height, _width, _time_multiplikator):
        self.time = 0
        self.time_multiplikator = _time_multiplikator
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)
        self.new_figure()

    def new_figure(self):
        self.figure = Figure(3, 0)

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def side(self, dx):
        old_x = self.figure.x
        edge = False
        for i in range(4):
            for j in range(4):
                p = i * 4 +j
                if p in self.figure.image():
                    if j + self.figure.x + dx > self.width - 1 or j + self.figure.x + dx < 0:
                        edge = True
        if not edge:
            self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def left(self):
        self.side(-1)

    def right(self):
        self.side(1)

    def down(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.figure.image():
                    try:
                        self.field[i + self.figure.y][j + self.figure.x]
                    except IndexError as ex:
                        for args in ex.args:
                            if args == "list index out of range":
                                return True

                    if i + self.figure.y > self.height - 1 or i + self.figure.y < 0 or self.field[i + self.figure.y][j + self.figure.x] > 0 or j + self.figure.x == -1:
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.type + 1
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.score += int((self.score / int(pygame.time.get_ticks() / 1000))*self.score*time_multiplikator)
            self.state = "gameover"

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i2 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i2][j] = self.field[i2 - 1][j]
        self.score += lines ** 2

    def getTime(self):
        if self.state == "gameover":
            return self.time
        time = int(pygame.time.get_ticks() / 1000)
        if time < 60:
            self.time = str(time) + " sec"
        elif time % 60 < 10:
            self.time = str(int(time / 60)) + ":0" + str(time % 60) + " min"
        else:
            self.time = str(int(time / 60)) + ":" + str(time % 60) + " min"
        return self.time



pygame.init()
screen = pygame.display.set_mode((380, 670))
pygame.display.set_caption("Tetris")

done = False
speed = 1
max_fps = 1000
clock = pygame.time.Clock()
counter = 0
zoom = 30
time_multiplikator = 1

game = Tetris(20, 10, time_multiplikator)
pressing_down = False
pressing_left = False
pressing_right = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

runs = 0


while not done:
    runs += 1
    if game.state == "start":
        if runs > int(clock.get_fps()) / speed:
            runs = 0
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if game.state == "start":
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    pressing_left = True
                if event.key == pygame.K_RIGHT:
                    pressing_right = True
        if game.state == "start":
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False
                if event.key == pygame.K_LEFT:
                    pressing_left = False
                if event.key == pygame.K_RIGHT:
                    pressing_right = False

            if pressing_down:
                game.down()
            if pressing_left:
                game.left()
            if pressing_right:
                game.right()

    screen.fill(color=WHITE)
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] == 0:
                color = GRAY
                just_border = 1
            else:
                color = colors[game.field[i][j]]
                just_border = 0
            pygame.draw.rect(screen, color, [30+j*zoom, 30+i*zoom, 1*zoom, 1*zoom], just_border)

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, game.figure.color, [30+(j + game.figure.x)*zoom, 30+(i + game.figure.y)*zoom, 1*zoom, 1*zoom])

    gameover_font = pygame.font.SysFont('Calibri', 65, True, False)
    text_gameover = gameover_font.render("Game Over!", True, (255, 0, 0))

    if game.state == "gameover":
        screen.blit(text_gameover, [5, 250])

    score_font = pygame.font.SysFont('Calibri', 25, True, False)
    text_score = score_font.render("Score: " + str(game.score), True, (0, 0, 0))
    screen.blit(text_score, [0, 0])

    score_time = pygame.font.SysFont('Calibri', 25, True, False)
    text_time = score_font.render("Time: " + game.getTime(), True, (0, 0, 0))
    screen.blit(text_time, [200, 0])

    pygame.display.flip()
    clock.tick(max_fps)


pygame.quit()
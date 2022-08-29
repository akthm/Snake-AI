import pygame
import random
GRID_SIZE = 20

WINDOW_SIZE = 500

RED = (255, 0, 0)

file = "results.txt"
class screen():
    def __init__(self,width,rows,start_state,obstacle_num=0,walls=[]):
        self.width = width
        self.rows = rows
        self.start = start_state
        self.obstacle_num = obstacle_num
        if walls == []:
            self.obs = []
            if obstacle_num!=0:
                self.generate_obstacles()
            self.wall = []
            self.generate_walls()
        else:
            self.wall = walls
            self.obs = walls
        self.win = pygame.display.set_mode((width, width))
    def generate_walls(self):
        if self.obs:
            self.wall += self.obs
        for i in range(GRID_SIZE):
            self.wall.append((i, 0))
            self.wall.append((0, i))
            self.wall.append((GRID_SIZE - 1, i))
            self.wall.append((i, GRID_SIZE - 1))
        return self.wall


    def generate_obstacles(self):
        for i in range(self.obstacle_num):
            x_rand = random.randrange(19)
            y_rand = random.randrange(19)
            self.obs.append((x_rand, y_rand))


    def redrawWindow(self, snake,snack):
        # global rows, width, snack
        self.win.fill((0, 0, 0))
        snake.draw(self.win)
        snack.draw(self.win)
        for obstacle in snake.obstacles:
            obstacle.draw(self.win)
        self.drawGrid()
        pygame.display.update()
        # print("yum:", food.pos)

    def drawGrid(self):
        sizeBtwn = self.width // self.rows
        x = 0
        y = 0
        for l in range(self.rows):
            x = x + sizeBtwn
            y = y + sizeBtwn
            pygame.draw.line(self.win, (255, 255, 255), (x, 0), (x, self.width))
            pygame.draw.line(self.win, (255, 255, 255), (0, y), (self.width, y))

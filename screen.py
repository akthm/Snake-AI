import pygame
import random
from cube import *


class Screen:

    def __init__(self,width,rows,start_state,obstacle_num=0,walls=False):
        self.width = width
        self.rows = rows
        self.start = start_state
        self.obstacle_num = obstacle_num
        self.obs = []
        self.wall = []
        self.generate_obstacles()
        if walls:
            self.generate_walls()
        self.win = pygame.display.set_mode((width, width))

    def generate_walls(self):
        for i in range(self.rows):
            self.wall.append((i, 0))
            self.wall.append((0, i))
            self.wall.append((self.rows - 1, i))
            self.wall.append((i, self.rows - 1))
        self.wall = list(set(self.wall))
        return self.wall

    def generate_obstacles(self):
        self.obs = []
        available = []
        for row in range(self.rows):
            for col in range(self.rows):
                if (row, col) not in self.wall:
                    available.append((row, col))
        for i in range(self.obstacle_num):
            self.obs.append(random.choice(available))

    def redrawWindow(self, snake, snack):
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

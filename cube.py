
GRID_SIZE = 20
WINDOW_SIZE = 500

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


START_POS = (2, 2)


file = "results.txt"
import pygame
import random


class cube(object):
    rows = GRID_SIZE
    w = WINDOW_SIZE

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        pos_x = self.pos[0] + self.dirnx
        if pos_x == -1:
            pos_x = GRID_SIZE - 1
        elif pos_x == GRID_SIZE:
            pos_x = 0
        pos_y = self.pos[1] + self.dirny
        if pos_y == -1:
            pos_y = GRID_SIZE - 1
        elif pos_y == GRID_SIZE:
            pos_y = 0
        self.pos = (pos_x, pos_y)

    def reset(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

    def get_pos(self):
        return self.pos[0],self.pos[1]


def randomSnack(rows, snake):
    positions = [cell.pos for cell in snake.body]
    positions += [cell.pos for cell in snake.obstacles]
    available = []
    for row in range(rows):
        for col in range(rows):
            if (row, col) not in positions:
                available.append((row, col))
    if not available:
        return available
    return random.choice(available)


# def randomSnack(rows, item, walls, obs):
#     positions = item.body
#     while True:
#         x = random.randrange(rows)
#         y = random.randrange(rows)
#         if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
#             continue
#         if len(list(filter(lambda z: z == (x, y), walls))) > 0:
#             continue
#         if len(list(filter(lambda z: z == (x, y), obs))) > 0:
#             continue
#         else:
#             break
#     return (x, y)
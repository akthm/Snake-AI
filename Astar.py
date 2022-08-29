# from snake import *
from Snake import randomSnack,actionsList,scoreList
import pygame

from heuristics import *
from Util import *
def aStar_search(s, i, slow, my_screen, heuristic,snack,tempFood,speedrun=False):
    # global width, rows, snack, tempFood, startState, food

    # my_screen = screen(WINDOW_SIZE,GRID_SIZE,START_POS)

    def performActions(dirs, slow):
        # perform actions in the game window so we can see the results
        for action in dirs:
            if slow:
                # pygame.time.delay(50)
                # clock.tick(90)
                pass
            s.moveAuto(action)
            my_screen.redrawWindow(s, snack)
    if speedrun:
        # print(i)
        snack.reset((i[0],i[1]), color=(0, 255, 0))
    else:

     snack.reset(randomSnack(my_screen.rows, s), color=(0, 255, 0))

    # tempFood = snack
    tempFood.reset(snack.pos, snack.dirnx, snack.dirny, snack.color)

    clock = pygame.time.Clock()
    flag = True

    aStar_priorityqueue = PriorityQueue()  # fringe
    visited = set()
    aStar_priorityqueue.push((s.getStartState(), [], 0), 0)

    while 1:
        if aStar_priorityqueue.isEmpty():
            break

        current, directions, costs = aStar_priorityqueue.pop()  # add costs for ucs
        # print("Current:", current)
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                s.score += 1
                s.addCube()
                performActions(directions, slow)
                # print("A_Star number of actions:", len(directions))
                actionsList[2].append(len(directions))
                # print("A_Star score:", len(s.body))
                scoreList[2] = len(s.body)
                # scoreList[2] = s.score
            for childNode, direction, cost in s.getSuccessors(current):
                if childNode not in aStar_priorityqueue.heap:
                    if childNode in visited:  # make sure child is not in visited so we don't go backwards
                        continue
                    hCost = costs + cost + heuristic(childNode,tempFood)
                    aStar_priorityqueue.push((childNode, directions + [direction], costs + cost), hCost)


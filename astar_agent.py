# from snake import *
from util import *


def aStar_search(snake, heuristic, speedrun=False):
    aStar_priorityqueue = PriorityQueue()  # fringe
    visited = set()
    aStar_priorityqueue.push((snake.getStartState(), [], 0), 0)
    while 1:
        if aStar_priorityqueue.isEmpty():
            break

        current, directions, costs = aStar_priorityqueue.pop()  # add costs for ucs
        # print("Current:", current)
        if current not in visited:
            visited.add(current)
            if snake.isGoalState(current):
                return directions

            for childNode, direction, cost in snake.getSuccessors(current):
                if childNode not in aStar_priorityqueue.heap:
                    if childNode in visited:  # make sure child is not in visited so we don't go backwards
                        continue
                    hCost = costs + cost + heuristic(childNode, snake.tmpFood)
                    aStar_priorityqueue.push((childNode, directions + [direction], costs + cost), hCost)
    return []

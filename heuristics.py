import sys
import inspect
import heapq, random


# from snake import tempFood



def manhattanDistance(xy1, xy2):
    """Returns the Manhattan distance between points xy1 and xy2"""
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


# added this function to test
def euclideanDistance(xy1, xy2):
    """The Euclidean distance heuristic for a PositionSearchProblem"""
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


def notDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    print("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
    sys.exit(1)


def nullHeuristic(state):
    # trivial heuristic
    return 0


def manhattanHeuristic(state):
    # uses distance as a score for heuristic
    xy1 = state.body[0]
    xy2 = state.food_pos
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclideanCost(state): # use a euclidean measurement to use as a cost
    xy1 = state.body[0]
    xy2 = state.food_pos
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

def normal_cost(state):
    return 1

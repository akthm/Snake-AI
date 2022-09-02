from util import *
from snake_state import SnakeState
from heuristics import *


def get_successors(current_state, cost_func=normal_cost):  # more like surrounding grid positions
    """returns a tuple of states, actions, costs"""

    '''Theoretically the max # of successors that can be generated at once should be 3: in front of the head,
    and the two sides of the head (if we have not eaten food yet we can have 4 successors). We will also make it so
    that the snake can not wrap around the screen.'''
    current_pos = current_state.body[0]
    successors = []
    left_state = SnakeState.get_next(current_state, "LEFT")
    if not left_state.is_terminated:
        successors.append((left_state, "LEFT", cost_func(current_state)))
    right_state = SnakeState.get_next(current_state, "RIGHT")
    if not right_state.is_terminated:
        successors.append((right_state, "RIGHT", cost_func(current_state)))
    up_state = SnakeState.get_next(current_state, "UP")
    if not up_state.is_terminated:
        successors.append((up_state, "UP", cost_func(current_state)))
    down_state = SnakeState.get_next(current_state, "DOWN")
    if not down_state.is_terminated:
        successors.append((down_state, "DOWN", cost_func(current_state)))
    return successors


def aStar_search(snake, heuristic, cost_func=normal_cost):
    fringe = PriorityQueue()  # fringe
    visited = set()
    fringe.push((snake.getStartState(), [], 0), 0)
    while 1:
        if fringe.isEmpty():
            break

        current_state, directions, costs = fringe.pop()  # add costs for ucs
        # print("Current:", current_state)
        if current_state.body[0] not in visited:
            visited.add(current_state.body[0])
            if current_state.is_goal_state():
                return directions

            for childNode, direction, cost in get_successors(current_state, cost_func):
                if childNode not in fringe.heap:
                    if childNode in visited:  # make sure child is not in visited so we don't go backwards
                        continue
                    hCost = costs + cost + heuristic(childNode)
                    fringe.push((childNode, directions + [direction], costs + cost), hCost)

    return []

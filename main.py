from argparse import ArgumentParser, FileType
import sys

import pygame.time

import snake
import time
from screen import *
from heuristics import *
from astar_agent import aStar_search
from hamiltonian import HamiltonianAgent
from snake import *
from qlearningAgent import SnakeQAgent, get_current_state
from cube import *
import numpy as np
from snake_state import SnakeState

DEFAULT_MODEL = "100000.pickle"

DELAY = 70

COST_MAPPER = {'normal': normal_cost, 'euclidean': euclideanCost}


def parse_command_line_args(args):
    """ Parse command-line arguments and organize them into a single structured object. """

    parser = ArgumentParser(
        description='Snake AI replay client.',
        epilog='Example: main.py --agent astar --heuristic manhattan '
    )

    parser.add_argument(
        '--interface',
        type=str,
        choices=['silent', 'gui'],
        default='gui',
        help='Interface mode (silent or GUI).',
    )
    parser.add_argument(
        '--agent',
        required=True,
        type=str,
        choices=['human', 'hamilton', 'astar', 'q-learning'],
        help='Player agent to use.',
    )
    parser.add_argument(
        '--heuristic',
        required=False,
        choices=['manhattan', 'null'],
        type=str,
        default='manhattan',
        help='Heuristic to use in A*.',
    )
    parser.add_argument(
        '--cost',
        required=False,
        choices=['normal', 'euclidean'],
        type=str,
        default='normal',
        help='cost func to use in A*.',
    )
    parser.add_argument(
        '--num_episodes',
        type=int,
        default=1,
        help='The number of episodes to run consecutively.',
    )

    parser.add_argument('--apples',
                        nargs=1,
                        type=FileType('r'),
                        help='insert apples locations using a file')

    parser.add_argument('--model',
                        type=str,
                        default=DEFAULT_MODEL,
                        help='q-learning model file (pickle)')

    parser.add_argument(
        '--ob',
        required=False,
        type=int,
        default=0,
        help='Number of Obstacles (default 0)',
    )

    parser.add_argument(
        '-w',
        required=False,
        action='store_true',
        help='Add walls',
    )
    parser.add_argument(
        '-t',
        required=False,
        action='store_true',
        help='train q-agent',
    )
    return parser.parse_args(args)


def play_human(snk, screen):
    my_screen = screen
    if not my_screen:
        print("ERROR: human should be played with gui")
        exit(1)
    s = snk
    # snack = cube(randomSnack(rows, s), color=(0, 255, 0))

    # tempFood = snack

    flag = True
    snk.gen_new_food()
    t0 = time.process_time()

    while flag:
        # for index, position in enumerate(s.walls):  # we can use this to see current walls (basically our body)
        #     print("Walls:", position.pos)
        pygame.time.delay(DELAY)
        s.move()
        if s.isGoalState(s.head.pos):
            s.score += 1
            s.addCube()
            snk.gen_new_food()
        if s.is_terminated():
            print('Score:', len(s.body))
            message_box("u die'd", "dead")
            s.reset((10, 10))
            break

        my_screen.redrawWindow(s, s.tmpFood)
    t1 = time.process_time()
    return s.score, t1 - t0


def performActions(dirs, snk, screen):
    # perform actions in the game window so we can see the results
    for action in dirs:
        snk.moveAuto(action)

        snk.next_move = action

        if snk.isGoalState(snk.head.pos):
            snk.addCube()
            snk.score += 1

        pygame.time.delay(DELAY)
        if screen:
            screen.redrawWindow(snk, snk.tmpFood)


def run_Astar(snk, screen, heuristic, cost):
    t0 = time.process_time()
    snk.gen_new_food()
    if screen:
        screen.redrawWindow(snk, snk.tmpFood)
    i = 0
    while i < snk.num_of_apples and not snk.is_terminated():
        directions = aStar_search(snk, heuristic, cost)
        performActions(directions, snk, screen)
        snk.gen_new_food()
        i += 1
    t1 = time.process_time()
    return snk.score,  t1 - t0


def run_qlearning(snk, scn, model_file):
    agent = SnakeQAgent(eps=0.001)
    snk.gen_new_food()
    agent.read_table(model_file)  # latest model
    last_act = ""
    current_length = snk.score + 1
    steps_unchanged = 0
    t0 = time.process_time()
    while not snk.is_terminated():
        pygame.time.delay(DELAY)
        if current_length != snk.score + 1:
            steps_unchanged = 0
            current_length = snk.score + 1
        else:
            steps_unchanged += 1

        state = get_current_state(snk)
        act = np.argmax(agent.values[state])
        if steps_unchanged == 1000:
            break
        action = ["LEFT", "RIGHT", "UP", "DOWN"][act]
        snk.next_move = action
        last_act = action
        reward = snk.moveAuto(action)

        if reward == 1:
            snk.score += 1
            snk.gen_new_food()
            snk.addCube()

        elif reward == -10:
            print("snake dies at " + str(snk.head.pos))
            pass
        if scn:
            scn.redrawWindow(snk, snk.tmpFood)
    t1 = time.process_time()
    return snk.score, t1 - t0


def runHamiltonian(snk, scn):
    agent = HamiltonianAgent(GRID_SIZE // 2 - 1, GRID_SIZE // 2 - 1)
    steps_with_no_food = 0
    snk.gen_new_food()
    t0 = time.process_time()
    while not snk.is_terminated():
        agent.next_move(snk)
        move = agent.get_direction()
        snk.next_move = move
        snk.moveAuto(move)
        steps_with_no_food += 1

        if snk.is_terminated():
            agent.reward(move, -1000)
        elif snk.isGoalState(snk.head.pos):
            snk.gen_new_food()
            snk.score += 1
            snk.addCube()
            steps_with_no_food = 0
            agent.reward(move, 10000)
        else:
            agent.reward(move, -20, after_hit=False)
        if steps_with_no_food > 1000:
            break
        if scn:
            scn.redrawWindow(snk, snk.tmpFood)
        pygame.time.delay(DELAY)
    t1 = time.process_time()
    return snk.score, t1 - t0


def train_q_learning(snk, scn, num_episodes):
    agent = SnakeQAgent(discount_rate=0.78, num_episodes=num_episodes)
    agent.train(snk, scn)


def main():
    parsed_args = parse_command_line_args(sys.argv[1:])
    if parsed_args.apples:
        apples = eval((parsed_args.apples[0]).readline())
    else:
        apples = None
    mysnake = Snake(RED, START_POS, apples)
    obs_num = parsed_args.ob
    walls = parsed_args.w
    myscreen = Screen(WINDOW_SIZE, GRID_SIZE, START_POS, obs_num, walls)
    mysnake.set_obstacles(myscreen.obs + myscreen.wall)
    tmpscreen = None
    if parsed_args.interface == "gui":
        tmpscreen = myscreen
    agent = parsed_args.agent
    scores = []
    times = []
    if parsed_args.t:
        train_q_learning(mysnake, tmpscreen, parsed_args.num_episodes)
        exit()
    for i in range(1, parsed_args.num_episodes + 1):
        score = 0
        timer = 0.0
        if agent == "human":
            score, timer = play_human(mysnake, tmpscreen)
        elif agent == "astar":
            heuris = nullHeuristic if parsed_args.heuristic == 'null' else manhattanHeuristic
            score, timer = run_Astar(mysnake, tmpscreen, heuris, COST_MAPPER[parsed_args.cost])
        elif agent == "q-learning":
            score, timer = run_qlearning(mysnake, tmpscreen, parsed_args.model)
        elif agent == "hamilton":
            if not parsed_args.w:
                myscreen.generate_walls()
                mysnake.set_obstacles(myscreen.wall + myscreen.obs)
            if parsed_args.ob:
                raise ValueError("Hamiltonian cannot work with obstacles")
            score, timer = runHamiltonian(mysnake, tmpscreen)
        times.append(timer)
        scores.append(score)
        mysnake.reset(START_POS)
        myscreen.generate_obstacles()
        mysnake.set_obstacles(myscreen.obs + myscreen.wall)
        if apples:
            line = (parsed_args.apples[0]).readline()
            try:
                apples = eval(line)
                mysnake.update_apples(apples)
            except SyntaxError:
                break

    print(times)
    print("average timer :",  np.mean(times))
    print(scores)
    print("average score :", np.mean(scores))


if __name__ == '__main__':
    main()

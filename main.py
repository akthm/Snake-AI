from argparse import ArgumentParser, FileType
import sys
import snake
from screen import *
import heuristics
from astar_agent import aStar_search
from hamiltonian import HamiltonianAgent
from snake import *
from qlearningAgent import SnakeQAgent, get_current_state
from cube import *


DELAY = 20
GRID_SIZE = 20



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
        '--num_episodes',
        type=int,
        default=1,
        help='The number of episodes to run consecutively.',
    )
    parser.add_argument('--apples', nargs=1,  type=FileType('r'),
                        help='insert apples locations using a file')
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
    return parser.parse_args(args)


def performActions(dirs, snk, screen, clock):
    # perform actions in the game window so we can see the results
    for action in dirs:
        snk.moveAuto(action)
        if snk.isGoalState(snk.head.pos):
            snk.addCube()
            snk.score += 1
            break
        pygame.time.delay(DELAY)
        clock.tick(60)
        screen.redrawWindow(snk, snk.tmpFood)


def run_Astar(snk, screen, heuristic):
    clock = pygame.time.Clock()
    screen.redrawWindow(snk, snk.tmpFood)
    for i in range(snk.num_of_apples):
        directions = aStar_search(snk, heuristic)
        performActions(directions, snk, screen, clock)

    return snk.score, clock.get_time()


def run_qlearning(snk, scn):
    clock = pygame.time.Clock()
    agent = SnakeQAgent(eps=0.001)
    snk.gen_new_food()
    agent.read_table("pickle/99500.pickle")  # latest model
    current_length = snk.score + 1
    steps_unchanged = 0
    while not snk.is_terminated():
        pygame.time.delay(DELAY)
        if current_length != snk.score + 1:
            steps_unchanged = 0
            current_length = snk.score + 1
        else:
            steps_unchanged += 1

        state = get_current_state(snk)
        act = agent.get_action(state)
        if steps_unchanged == 1000:
            break
        action = ["LEFT", "RIGHT", "UP", "DOWN"][act]
        snk.next_move = action
        reward = snk.moveAuto(action)

        if reward == 1:
            snk.score += 1
            snk.gen_new_food()
            snk.addCube()

        elif reward == -10:
            print("snake dies at " + str(snk.head.pos))
            pass

        scn.redrawWindow(snk, snk.tmpFood)
        clock.tick(90)
    return snk.score, clock.get_time()


def runHamiltonian(snk, scn):
    agent = HamiltonianAgent(scn.rows // 2 - 1, scn.rows // 2 - 1)
    clock = pygame.time.Clock()
    steps_with_no_food = 0
    i = 0
    snk.gen_new_food()
    # if apples:
    #     snack.reset((apples[i][0],apples[i][1]), color=(0, 255, 0))
    #     # tempFood = snack
    # else:
    #     snack.reset(randomSnack(scn.rows, snk, scn.getWalls(), scn.getObstacles()), color=(0, 255, 0))
    # tempFood.reset(snack.pos, snack.dirnx, snack.dirny, snack.color)

    while not snk.is_terminated():
        agent.next_move(snk)
        move = agent.get_direction()
        snk.next_move = move
        snk.moveAuto(move)
        steps_with_no_food += 1

        if snk.is_terminated():
            agent.reward(move, -1000)
        elif snk.isGoalState(snk.head.pos):
            # if apples:
            #     i+=1
            #     if i >= len(apples):
            #         break
            #     else:
            #         snack.reset((apples[i][0],apples[i][1]), color=(0, 255, 0))
            # else:
            #     snack.reset(randomSnack(scn.rows, snk, scn.getWalls(), scn.getObstacles()), color=(0, 255, 0))
            # # tempFood = snack
            # tempFood.reset(snack.pos, snack.dirnx, snack.dirny, snack.color)
            snk.gen_new_food()
            snk.score += 1
            snk.addCube()
            steps_with_no_food = 0
            agent.reward(move, 10000)
        else:
            agent.reward(move, -20, after_hit=False)
        if steps_with_no_food > 1000:
            break
        scn.redrawWindow(snk, snk.tmpFood)
        clock.tick(60)
    return snk.score, clock.get_time()


def main():
    parsed_args = parse_command_line_args(sys.argv[1:])
    if parsed_args.apples:
        apples = eval((parsed_args.apples[0]).readline())
    else:
        apples = None
    mysnake = Snake(RED, START_POS, apples)
    myscreen = None
    if parsed_args.interface == "gui":
        obs_num = parsed_args.ob
        walls = parsed_args.w
        myscreen = Screen(WINDOW_SIZE, GRID_SIZE, START_POS, obs_num, walls)
        mysnake.set_obstacles(myscreen.obs + myscreen.wall)

    agent = parsed_args.agent
    scores = []
    times = []
    for i in range(1, parsed_args.num_episodes + 1):
        score = 0
        time = 0.0
        if agent == "human":
            snake.main()
        elif agent == "astar":
            heuris = heuristics.nullHeuristic if parsed_args.heuristic == 'null' else heuristics.manhattanHeuristic
            score, time = run_Astar(mysnake, myscreen, heuris)
        elif agent == "q-learning":
            score, time = run_qlearning(mysnake, myscreen)
        elif agent == "hamilton":
            if not parsed_args.w:
                myscreen.generate_walls()
                mysnake.set_obstacles(myscreen.wall)
            if parsed_args.ob:
                raise ValueError("Hamiltonian cannot work with obstacles")
            score, time = runHamiltonian(mysnake, myscreen)
        times.append(time)
        scores.append(score)
        mysnake.reset(START_POS)
    print(times)  # todo check time measurement currently not correct
    print(scores)


if __name__ == '__main__':
    main()

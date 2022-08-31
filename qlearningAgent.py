
import random

import pygame.time

import heuristics
import pickle
import numpy as np
from astar_agent import aStar_search

MOVES = ("LEFT", "RIGHT", "UP", "DOWN")


def get_current_state(snk):
    snake_pos = snk.head.pos
    fruit_position = snk.tmpFood.pos
    state = []
    move = snk.next_move
    for legal_move in MOVES:
        state.append(int(move == legal_move))
    state.append(int(fruit_position[0] < snake_pos[0]))
    state.append(int(fruit_position[0] > snake_pos[0]))
    state.append(int(fruit_position[1] < snake_pos[1]))
    state.append(int(fruit_position[1] > snake_pos[1]))
    for action in MOVES:
        new_pos = snk.get_new_position(action)
        state.append(int(snk.will_terminate(new_pos)))
    return tuple(state)


class SnakeQAgent:
    def __init__(self, discount_rate=0.95, learning_rate=0.01, eps=1.0, eps_discount=0.9992, min_eps=0.001,
                 num_episodes=1000):
        self.survived = []
        self.score = []
        self.num_episodes = num_episodes
        self.min_eps = min_eps
        self.eps_discount = eps_discount
        self.eps = eps
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.values = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))

    @staticmethod
    def find_action(action):
        if action == "LEFT":
            return 0
        elif action == "RIGHT":
            return 1
        elif action == "UP":
            return 2
        else:
            return 3

    def get_astar_action(self, state, snake):
        if random.random() < self.eps:
            directions = aStar_search(snake, heuristics.nullHeuristic)
            for direction in directions:
                return self.find_action(direction)
        return np.argmax(self.values[state])

    def get_action(self, state):
        if random.random() < self.eps:
            return random.choice([0, 1, 2, 3])
        return np.argmax(self.values[state])

    def read_table(self, filename):
        with open(filename, 'rb') as file:
            table = pickle.load(file)
        self.values = table

    def write_table(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.values, file)

    def train(self, snake, screen=None):
        for i in range(1, self.num_episodes + 1):
            steps_without_food = 0

            # print updates
            if i % 25 == 0:
                print(
                    f"Episodes: {i}, score: {np.mean(self.score)}, survived: {np.mean(self.survived)}, eps: {self.eps}, lr: {self.learning_rate}")
                self.score = []
                self.survived = []

            # occasionally save latest model
            if (i < 500 and i % 10 == 0) or (i >= 500 and i < 1000 and i % 200 == 0) or (i >= 1000 and i % 500 == 0):
                self.write_table(f'pickle/{i}.pickle')

            current_state = get_current_state(snake)

            self.eps = max(self.eps * self.eps_discount, self.min_eps)
            done = False
            snake.gen_new_food(None)
            while not done:
                act = self.get_action(current_state)
                action = ["LEFT", "RIGHT", "UP", "DOWN"][act]
                snake.next_move = action
                reward = snake.moveAuto(action)
                new_state = get_current_state(snake)

                self.values[current_state][act] = (1 - self.learning_rate) \
                                                    * self.values[current_state][act] + self.learning_rate \
                                                    * (reward + self.discount_rate * max(self.values[new_state]))
                current_state = new_state
                steps_without_food += 1
                if reward == 1:
                    steps_without_food = 0
                    snake.addCube()
                    snake.score += 1
                    snake.gen_new_food(None)

                elif reward == -10:
                    done = True

                if steps_without_food == 1000:
                    break
            if screen:
                pygame.time.delay(40)
                screen.redrawWindow(snake, snake.tmpFood)
            self.score.append(snake.score)
            self.survived.append(not snake.is_terminated())
            snake.reset(snake.START_POS)
            snake.gen_new_food()

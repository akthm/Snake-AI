import copy
import cube


class SnakeState:
    def __init__(self, snake):
        self.body = [cell.pos for cell in snake.body]
        self.food_pos = snake.tmpFood.pos
        self.obs = [cell.pos for cell in snake.obstacles]
        self.is_terminated = snake.is_terminated()

    @staticmethod
    def get_next(snake_state, action):
        new_state = copy.deepcopy(snake_state)
        dirnx = 0
        dirny = 0
        if action == "LEFT":
            dirnx = -1
            dirny = 0

        elif action == "RIGHT":
            dirnx = 1
            dirny = 0

        elif action == "UP":
            dirnx = 0
            dirny = -1

        elif action == "DOWN":
            dirnx = 0
            dirny = 1

        tmp_pos = new_state.body[0]
        new_x = new_state.body[0][0] + dirnx
        new_y = new_state.body[0][1] + dirny
        if new_x == -1:
            new_x = cube.GRID_SIZE - 1
        elif new_x == cube.GRID_SIZE:
            new_x = 0
        if new_y == -1:
            new_y = cube.GRID_SIZE - 1
        elif new_y == cube.GRID_SIZE:
            new_y = 0
        new_pos = (new_x, new_y)
        new_state.body[0] = new_pos

        for cell_pos in new_state.body[1:]:
            other_tmp = cell_pos
            cell_pos = tmp_pos
            tmp_pos = other_tmp

        all_block_list = [pos for pos in new_state.body]
        all_block_list += [pos for pos in new_state.obs]
        new_state.is_terminated = len(all_block_list) != len(set(all_block_list))

        return new_state

    def is_goal_state(self):
        return self.body[0] == self.food_pos

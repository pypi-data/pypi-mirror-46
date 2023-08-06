import random
from collections import deque
from gridworlds.environment import Env
from gridworlds.grid import Grid
from math import inf


"""
This agent has an internal mapping of the environment so can set the state and perform actions on that given state
which is not common but simply for learning purposes.
"""

invalid_start_states = {(1, 1), (0, 3), (1, 3)}


class ValueIterationAgent:

    grid_rep = """

    | 0 | 0 | 0 | 1 |
    | 0 | 2 | 0 | 3 |
    | 0 | 0 | 0 | 0 |  

               """

    def __init__(self, rows, cols, action_space, epsilon=0.5, gamma=0.9, converge_threshold=1):
        self.state_values = self.get_init_state_values(rows, cols)
        self.state_space = [(row, col) for row in range(rows) for col in range(cols)]
        self.action_space = action_space
        self.epsilon = epsilon
        self.gamma = gamma
        self.converge_threshold = converge_threshold

        self.policy = self.get_random_policy(rows, cols)
        self.memory = deque()

    def get_init_state_values(self, rows, cols):
        state_values = {}
        for row in range(rows):
            for col in range(cols):
                    key = str(row) + ' ' + str(col)
                    state_values[key] = 0.0

        return state_values

    def get_random_policy(self, rows, cols):
        policy = {}
        for row in range(rows):
            for col in range(cols):
                key = str(row) + ' ' + str(col)
                policy[key] = random.choice(self.action_space)

        return policy

    def get_policy_key(self, state):
        return str(state[0]) + ' ' + str(state[1])

    def act(self, state):
        if random.random() <= self.epsilon:
            return random.choice(self.action_space)
        else:
            return self.policy[self.get_policy_key(state)]

    def memorise(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def learn_state_values(self):

        max_delta = 0
        for state in self.state_space:
            if state in invalid_start_states:
                continue

            max_value = -inf
            old_value = self.get_state_value(state)
            for action in self.action_space:
                self.set_state(state)
                next_state, reward, done, info = self.env.step(action)

                new_value = reward + self.gamma * self.get_state_value(next_state)
                if new_value > max_value:
                    max_value = new_value
            state_value_delta = abs(max_value - old_value)
            if state_value_delta > max_delta:
                max_delta = state_value_delta

            self.update_state_value(state, max_value)

        # Stop training after change in value function is at a threshold
        if max_delta <= self.converge_threshold:
            return False
        else:
            return True

    def get_state_value(self, state):
        return self.state_values[str(state[0]) + ' ' + str(state[1])]

    def update_state_value(self, state, new_value):
        self.state_values[str(state[0]) + ' ' + str(state[1])] = new_value

    def update_policy(self):

        for state in self.state_space:
            if state in invalid_start_states:
                continue
            new_policy = None
            max_value = -inf
            for action in self.action_space:

                self.set_state(state)
                next_state, reward, _, _ = self.env.step(action)

                value = reward + self.gamma * self.get_state_value(next_state)
                if value > max_value:
                    new_policy = action
                    max_value = value

            self.policy[self.get_policy_key(state)] = new_policy

    def set_state(self, state):
        self.env = Env(Grid.generate_from_rep(3, 4, grid_rep), agent_start_pos=state, render=False, off_grid_penalty=-1)


if __name__ == "__main__":

    grid_rep = """

    | 0 | 0 | 0 | 1 |
    | 0 | 2 | 0 | 3 |
    | 0 | 0 | 0 | 0 |  

               """

    grid = Grid.generate_from_rep(3, 4, grid_rep)
    env = Env(grid, agent_start_pos=(2, 0), render=False, off_grid_penalty=-1)

    agent = ValueIterationAgent(3, 4, env.get_action_space())
    training = True
    iteration = 0
    while training:
        print("Iteration {}".format(iteration))
        training = agent.learn_state_values()
        agent.update_policy()
        iteration += 1
    print("\n\n")

    # Print policy
    policy_to_direction = {
        0: 'up',
        1: 'right',
        2: 'down',
        3: 'left'
    }
    str_builder = ""
    for row in range(3):
        str_builder += "|"
        for col in range(4):

            if (row, col) in ((1, 1), (1, 3)):
                str_builder += " {:5s} |".format("  X")
                continue
            elif (row, col) == (0, 3):
                str_builder += " {:5s} |".format("GOAL")
                continue

            policy = agent.policy[agent.get_policy_key((row, col))]
            direction = policy_to_direction[policy]
            str_builder += " {:5s} |".format(direction)
        str_builder += "\n"
    print(str_builder)
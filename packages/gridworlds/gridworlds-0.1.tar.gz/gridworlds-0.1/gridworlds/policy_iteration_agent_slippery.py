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

class PolicyIterationAgent:

    grid_rep = """

    | 0 | 0 | 0 | 1 |
    | 0 | 2 | 0 | 3 |
    | 0 | 0 | 0 | 0 |  

               """

    def __init__(self, rows, cols, action_space, epsilon=0.5, gamma=0.9):
        self.state_values = self.get_init_state_values(rows, cols)
        self.state_space = [(row, col) for row in range(rows) for col in range(cols)]
        self.action_space = action_space
        self.epsilon = epsilon
        self.gamma = gamma

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

        self.state_values = {k: 0.0 for k, _ in self.state_values.items()}
        for state in self.state_space:
            if state in invalid_start_states:
                continue

            for chosen_action in self.action_space:
                new_value = 0
                for actual_action in self.action_space:
                    self.set_state(state)
                    next_state, reward, done, info = self.env.step(actual_action)

                    if chosen_action == actual_action:
                        transition_prob = 0.7
                    else:
                        transition_prob = 0.3 / 3

                    new_value += transition_prob * (reward + self.gamma * self.get_state_value(next_state))
                self.update_state_value(state, new_value)


    def get_state_value(self, state):
        return self.state_values[str(state[0]) + ' ' + str(state[1])]

    def update_state_value(self, state, new_value):
        self.state_values[str(state[0]) + ' ' + str(state[1])] = new_value

    def policy_iteration(self):

        has_changed = False
        for state in self.state_space:
            if state in invalid_start_states:
                continue
            old_policy = self.policy[self.get_policy_key(state)]
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
            if new_policy != old_policy:
                has_changed = True

        return has_changed

    def set_state(self, state):
        self.env = Env(Grid.generate_from_rep(3, 4, grid_rep), agent_start_pos=state, render=False, off_grid_penalty=-1)


if __name__ == "__main__":

    grid_rep = """

    | 4 | 4 | 4 | 1 |
    | 4 | 2 | 4 | 3 |
    | 4 | 4 | 4 | 4 |  

               """

    grid = Grid.generate_from_rep(3, 4, grid_rep)
    env = Env(grid, agent_start_pos=(2, 0), render=False, off_grid_penalty=-1)

    agent = PolicyIterationAgent(3, 4, env.get_action_space())
    training = True
    iteration = 0
    while training:
        print("Iteration {}".format(iteration))
        agent.learn_state_values()
        training = agent.policy_iteration()
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
from gridworlds.grid import Grid
from gridworlds.environment import Env


def grid_from_string():

    grid_rep = """
    
    | 0 | 0 | 0 | 1 |
    | 0 | 2 | 0 | 3 |
    | 0 | 0 | 0 | 0 |  
           
               """

    grid = Grid.generate_from_rep(3, 4, grid_rep)
    env = Env(grid, agent_start_pos=(2, 0))
    for i in range(100):
        env.step(i % 4)

if __name__ == "__main__":
    grid_from_string()
import pygame
import random

from gridworlds.grid import Grid
from gridworlds.environment_exceptions import InvalidActionException


class Env:

    WIDTH = 750
    HEIGHT = 750

    MARGIN_TOP_PERC = 10
    MARGIN_BOTTOM_PERC = 10
    MARGIN_RIGHT_PERC = 10
    MARGIN_LEFT_PERC = 10

    LINE_COLOR = (0, 0, 0)
    LINE_WIDTH = 2

    DEFAULT_FONT = "arial"

    AGENT_COLOR = (0, 0, 255)
    _ACTION_SPACE = (0, 1, 2, 3)

    def __init__(self, grid, agent_start_pos=None, render=True, **kwargs):
        self.window_width, self.window_height = Env.WIDTH, Env.HEIGHT

        self.render = render
        self.margin_top_perc = Env.MARGIN_TOP_PERC
        self.margin_bottom_perc = Env.MARGIN_BOTTOM_PERC
        self.margin_right_perc = Env.MARGIN_RIGHT_PERC
        self.margin_left_perc = Env.MARGIN_LEFT_PERC
        self.agent_color = Env.AGENT_COLOR
        self.line_width = Env.LINE_WIDTH
        self.line_color = Env.LINE_COLOR
        self.font_name = Env.DEFAULT_FONT

        self.off_grid_penalty = 0
        self.off_grid_terminal = False
        self._override_options(kwargs)
        self._grid = grid

        if agent_start_pos:
            self._agent_tile = self._grid.get_tile(agent_start_pos[0], agent_start_pos[1])
        else:
            self._agent_tile = self.randomise_agent_position()
        self._running = False
        self._size = self.window_width, self.window_height

        self.grid_width, self.grid_height = self._calculate_board_size()
        self.tile_width, self.tile_height = self._calculate_tile_size()
        self.agent_pos = self._calc_agent_pos()
        self.state = self._agent_tile.get_state_rep()

        self.font = None
        self.stats = {
            'score': 0,
            'steps': 0
        }

        if self.on_init() == False:
            self._running = False

    def on_init(self):
        if self.render:
            pygame.init()
            pygame.font.init()
            self.font = pygame.font.SysFont(self.font_name, 30)

            self._display = pygame.display.set_mode(self._size, 0, 32)
            pygame.display.set_caption("Gridworld")
        self._running = True

    def _override_options(self, kwargs):
        for key, value in kwargs.items():
            # do not override internals
            if key[0] != '_':
                setattr(self, key, value)

    def randomise_agent_position(self):
        return random.choice(self._grid.get_valid_start_tiles())

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def update_env(self):
        if self.render:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self._draw()
            pygame.display.update()

    def step(self, action):
        if not action in Env._ACTION_SPACE:
            raise InvalidActionException(
                "Action {} invalid. Must be a integer within action space {}".format(action, Env._ACTION_SPACE))

        action = self._agent_tile.on_leave(self._grid.get_tiles, self.get_action_space(), action)

        if self.is_move_within_grid(action):
            self._move(action)
            self._agent_tile.on_land(self._grid.get_tiles())
            self.state = self._agent_tile.get_state_rep()
            self.update_env()
            reward = self._agent_tile.get_reward()
            self.update_stats(reward)
            return self.get_state(), reward, self._agent_tile.get_terminal(), self._agent_tile.get_info()

        else:
            self.update_stats(self.off_grid_penalty)
            return self.get_state(), self.off_grid_penalty, self.off_grid_terminal, self._agent_tile.get_info()

    def update_stats(self, reward):
        self.stats['score'] += reward
        self.stats['steps'] += 1

    def glimpse(self):
        self.update_env()

    def get_state(self):
        return self.state

    def get_state_space(self):
        return (tile.get_state_rep() for tile in self._grid.get_tiles)

    def get_action_space(self):
        return self._ACTION_SPACE

    def _move(self, action):
        # up
        if action == 0:
            self.agent_pos = (self.agent_pos[0], self.agent_pos[1] - self.tile_height)
            self._agent_tile = self._grid.get_tile(self._agent_tile.row - 1, self._agent_tile.col)

        # right
        elif action == 1 and self._agent_tile.col < self._grid.cols - 1:
            self.agent_pos = (self.agent_pos[0] + self.tile_width, self.agent_pos[1])
            self._agent_tile = self._grid.get_tile(self._agent_tile.row, self._agent_tile.col + 1)

        # down
        elif action == 2 and self._agent_tile.row < self._grid.rows -1:
            self.agent_pos = (self.agent_pos[0], self.agent_pos[1] + self.tile_height)
            self._agent_tile = self._grid.get_tile(self._agent_tile.row + 1, self._agent_tile.col)

        # left
        elif action == 3 and self._agent_tile.col > 0:
            self.agent_pos = (self.agent_pos[0] - self.tile_width, self.agent_pos[1])
            self._agent_tile = self._grid.get_tile(self._agent_tile.row, self._agent_tile.col - 1)

    def is_move_within_grid(self, action):
        return (action == 0 and self._agent_tile.row > 0) or \
                action == 1 and self._agent_tile.col < self._grid.cols - 1 or \
                action == 2 and self._agent_tile.row < self._grid.rows -1 or \
                action == 3 and self._agent_tile.col > 0


    def _calc_agent_pos(self):
        grid_offset_x = self.window_width * self.margin_left_perc / 100
        grid_offset_y = self.window_height * self.margin_top_perc / 100
        x_pos = grid_offset_x + self.tile_width * self._agent_tile.col + self.tile_width / 2
        y_pos = grid_offset_y + self.tile_height * self._agent_tile.row + self.tile_height / 2
        return x_pos, y_pos


    def _calculate_board_size(self):
        grid_width = self.window_width - self.window_width * ((self.margin_right_perc + self.margin_left_perc) / 100)
        grid_height = self.window_height - self.window_height * ((self.margin_top_perc + self.margin_bottom_perc) / 100)
        return grid_width, grid_height

    def _calculate_tile_size(self):
        return self.grid_width / self._grid.cols, self.grid_height / self._grid.rows

    def _draw(self):
        self._display.fill((255, 255, 255))
        self._draw_grid_border()
        self._draw_tiles()
        self._draw_agent()
        self._draw_stats()

    def _draw_grid_border(self):
        x_start = self.window_width * self.margin_left_perc / 100
        y_start = self.window_height * self.margin_top_perc / 100
        pygame.draw.rect(self._display, self.line_color, (
            x_start, y_start, self.grid_width, self.grid_height), self.line_width)

    def _draw_tiles(self):
        grid_offset_x = self.window_width * self.margin_left_perc / 100
        grid_offset_y = self.window_height * self.margin_top_perc / 100

        for row in range(self._grid.rows):
            for col in range(self._grid.cols):

                # draw outline
                pygame.draw.rect(self._display, self.line_color, (
                        grid_offset_x + (self.tile_width * col),
                        grid_offset_y + (self.tile_height * row),
                        self.tile_width, self.tile_height))

                # fill inner
                pygame.draw.rect(self._display, self._grid.get_tile(row, col).color, (
                        grid_offset_x + (self.tile_width * col) + self.line_width,
                        grid_offset_y + (self.tile_height * row) + self.line_width,
                        self.tile_width - self.line_width, self.tile_height - self.line_width))

    def _draw_agent(self):
        pygame.draw.circle(self._display, self.agent_color, (int(self.agent_pos[0]), int(self.agent_pos[1])), int(self.tile_width / 4))

    def _draw_stats(self):
        textsurface = self.font.render('Score: {}        Steps: {}'.format(self.stats['score'], self.stats['steps']), False, (0, 0, 0))
        self._display.blit(textsurface, (20, 20))


if __name__ == "__main__":
    grid = Grid.generate(5, 5)
    env = Env(grid)
    env.on_execute()

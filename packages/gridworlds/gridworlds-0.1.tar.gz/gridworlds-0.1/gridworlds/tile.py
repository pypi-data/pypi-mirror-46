from enum import Enum
import random


class TileType(Enum):
    EMPTY = 0
    GOAL = 1
    HOLE = 2
    PENALTY = 3
    SLIPPERY = 4


class Autonomy(Enum):
    FULL = 0
    PARTIAL = 1
    NONE = 2


class Tile:

    def __init__(self, row, col, tile_type=TileType.EMPTY, reward=0, autonomy=Autonomy.NONE,
                 resist_prob=0.5, color=(255, 255, 255), **kwargs):
        self.tile_type = tile_type
        self.row = row
        self.col = col
        self.autonomy = autonomy
        self.resist_prob = resist_prob
        self.color = color
        self.reward = reward
        self.info = None

        self.valid_start = True
        self.traversable = True
        self.terminal = False
        self.init_options(kwargs)

    def get_reward(self):
        return self.reward

    def get_terminal(self):
        return self.terminal

    def get_info(self):
        return None

    def get_state_rep(self):
        return self.row, self.col

    def init_options(self, options):
        for key, value in options.items():
            # do not override internals
            if key[0] != '_':
                setattr(self, key, value)

    def on_leave(self, tiles, action_space, action) -> int:
        return action

    def on_land(self, tiles):
        pass

    def update_request(self, behavior_overrides):
        if self.autonomy == Autonomy.FULL:
            return

        elif self.autonomy == Autonomy.PARTIAL and self.resist_prob > random.random():
            return

        else:
            for key, value in behavior_overrides.items():
                # do not override internals
                if key[0] != '_':
                    setattr(self, key, value)

class SlipperyTile(Tile):

    def __init__(self, row, col, tile_type=TileType.EMPTY, reward=0, autonomy=Autonomy.NONE,
                 resist_prob=0.5, color=(255, 255, 255), slippiness=0.3, **kwargs):
        super(SlipperyTile, self).__init__(row, col, tile_type=tile_type, reward=reward, autonomy=autonomy,
                 resist_prob=resist_prob, color=color, **kwargs)
        self.slippiness = slippiness

    def on_leave(self, tiles, action_space, action) -> int:
        if self.slippiness > random.random():
            return random.choice(action_space)
        else:
            return action

class TileGenerator:

    def __init__(self):
        pass

    @classmethod
    def create_from_type(cls, row, col, tile_type: TileType):
        if tile_type == TileType.EMPTY: return TileGenerator.create_empty(row, col)
        if tile_type == TileType.GOAL: return TileGenerator.create_goal(row, col)
        if tile_type == TileType.HOLE: return TileGenerator.create_hole(row, col)
        if tile_type == TileType.PENALTY: return TileGenerator.create_penalty(row, col)
        if tile_type == TileType.SLIPPERY: return TileGenerator.create_slippery(row, col)

    @classmethod
    def create_empty(cls, row, col):
        return Tile(row, col)

    @classmethod
    def create_goal(cls, row, col):
        return Tile(row, col, TileType.GOAL, reward=1, autonomy=Autonomy.FULL, color=(0, 255, 0),
                    valid_start=False, terminal=True)

    @classmethod
    def create_hole(cls, row, col):
        return Tile(row, col, TileType.HOLE, reward=-1, autonomy=Autonomy.FULL, color=(0, 0, 0),
                    valid_start=False, terminal=True)

    @classmethod
    def create_penalty(cls, row, col):
        return Tile(row, col, TileType.PENALTY, reward=-1, autonomy=Autonomy.FULL, color=(255, 0, 0),
                    valid_start=False, terminal=False)

    @classmethod
    def create_slippery(cls, row, col):
        return Tile(row, col, TileType.SLIPPERY, reward=0, autonomy=Autonomy.FULL, color=(0, 0, 125),
                    valid_start=True, terminal=False)
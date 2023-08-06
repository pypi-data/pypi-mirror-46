import operator
from typing import Dict

from gridworlds.grid_exceptions import *
from gridworlds.tile import *


class Grid:

    MIN_DIM = 2
    MAX_DIM = 100

    default_dict = {
        TileType.GOAL: 1,
        TileType.HOLE: 1,
        TileType.EMPTY: -1
    }

    def __init__(self, rows, cols):
        self._tiles = None
        self.rows = rows
        self.cols = cols
        self.traversable = None
        self.valid_starts = None

    def insert_tile(self, row, col, tile):
        if row > self.rows or col > self.cols:
            raise GridOutOfBoundsException("Unable to add tile at position ({},{}) for a grid with dimensions {}*{}".format(
                row, col, self.rows, self.cols))
        self._tiles[row][col] = tile

    def get_tile(self, row, col):
        return self._tiles[row][col]

    def get_tiles(self):
        return self._tiles

    def get_traversables(self):
        if self.traversable == None:
            self.traversable = [tile for tile in sum(self._tiles, []) if tile.traversable]
        return self.traversable

    def get_valid_start_tiles(self):
        if self.valid_starts == None:
            self.valid_starts = [tile for tile in sum(self._tiles, []) if tile.valid_start]
        return self.valid_starts

    @classmethod
    def generate(cls, rows, cols):
        return cls.generate_from_counts(rows, cols, cls.default_dict)

    @classmethod
    def generate_from_counts(cls, rows, cols, counts: Dict[TileType, int]):
        grid_positions = cls._get_shuffled_positions(rows, cols)

        specified = {k: v for k, v in counts.items() if v > 0}
        unspecified = [k for k, v in counts.items() if v < 0]

        total_specified = sum(specified.values())
        tiles_available = rows * cols
        if total_specified > tiles_available:
            raise GridGenerateException("The total count of explicitly specified tiles must be equal to or less than"
                                        "the number of rows * cols. \n"
                                        "\tTiles required: {}\n"
                                        "\tTiles available: {}".format(total_specified, tiles_available))

        grid = Grid(rows, cols)
        grid._tiles = [[None for _ in range(cols)] for _ in range(rows)]
        # prioritize filling grid with specified counts
        for tile_type, count in specified.items():
            for i in range(count):
                position = grid_positions.pop()
                grid.insert_tile(position['row'], position['col'],
                                 TileGenerator.create_from_type(position['row'], position['col'], tile_type))

        # fill remainder positions by randomly selecting from unspecified tiles
        for i in range(len(grid_positions)):
            position = grid_positions.pop()
            grid.insert_tile(position['row'], position['col'],
                             TileGenerator.create_from_type(position['row'], position['col'], random.choice(unspecified)))

        return grid

    @classmethod
    def generate_from_probabilities(cls, rows, cols, probabilities: Dict[TileType, float]):
        pass # todo

    """
    Generates a grid from a string representation. Create a grid using the pipe | to separate columns and newlines to
    separate rows. Numbers will be mapped to the Enum class TileType. Whitespace between columns is ignored.
    
    | 2 | 2 | 2 |
    | 1 | 1 | 2 |
    | 0 | 2 | 2 |
    
    """
    @classmethod
    def generate_from_rep(cls, rows, cols, representation: str):
        grid_positions = cls._get_positions(rows, cols)
        grid_positions.reverse() # so we can pop in reverse order (0, 0) first
        grid = Grid(rows, cols)
        grid._tiles = [[None for _ in range(cols)] for _ in range(rows)]

        rows = list(filter(operator.methodcaller('strip'), representation.split("\n")))
        for row in rows:
            cols = [col.replace(" ", "") for col in row.split("|")][1: -1]
            for col in cols:
                position = grid_positions.pop()
                grid.insert_tile(position['row'], position['col'],
                                 TileGenerator.create_from_type(position['row'], position['col'], TileType(int(col))))

        return grid

    @classmethod
    def _get_positions(cls, rows, cols):
        positions = [{'row': i, 'col': j} for i in range(rows) for j in range(cols)]
        return positions

    @classmethod
    def _get_shuffled_positions(cls, rows, cols):
        positions = Grid._get_positions(rows, cols)
        random.shuffle(positions)
        return positions

    @classmethod
    def _validate_dims(cls, rows, cols):
        if rows < Grid.MIN_DIM or cols < Grid.MIN_DIM:
            raise InvalidDimensionsException(
                "Input dimensions for rows ({}) and columns ({}) must be at least {}".format(rows, cols, Grid.MIN_DIM))

        if rows > Grid.MAX_DIM or cols > Grid.MAX_DIM:
            raise InvalidDimensionsException(
                "Input dimensions for rows ({}) and columns ({}) can be no more than {}".format(rows, cols, Grid.MAX_DIM))

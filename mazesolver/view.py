import enum
import time

import arcade as arc

from maze import Maze
from grid import Grid
from player import Player

RAW_MAZE_SHAPE = 12, 24

SCALE = 0.44
BLOCK_SIZE = 64

TEXTURE_WALL = ":resources:images/topdown_tanks/tileGrass1.png"
TEXTURE_PATH = ":resources:images/topdown_tanks/tileSand1.png"

FLAG_START = ":resources:images/items/flagRed1.png"
FLAG_STOP = ":resources:images/items/flagGreen2.png"

FLAG_SCALE = 0.16


class BlockType:
    WALL = 0
    PATH = 1


class View(arc.View):
    def __init__(self, window=None):
        super().__init__(window)

        self.maze = None
        self.grid = None

        self.walls = None
        self.path = None

        self.flags = None
        self.flag_start = None
        self.flag_stop = None

        self.actors = None
        self.player = None

        self.physics_engine = None

    def setup(self):
        self.maze = Maze.generate(RAW_MAZE_SHAPE, seed=int(time.time()))
        self.grid = Grid(self.maze.shape, BLOCK_SIZE, SCALE)

        self.walls = arc.SpriteList(use_spatial_hash=True)
        self.path = arc.SpriteList(use_spatial_hash=True)

        self.setup_maze()

        self.flags = arc.SpriteList(use_spatial_hash=True)
        self.flag_start = arc.Sprite(FLAG_START, scale=FLAG_SCALE)
        self.flags.append(self.flag_start)
        self.flag_stop = arc.Sprite(FLAG_STOP, scale=FLAG_SCALE)
        self.flags.append(self.flag_stop)

        self.set_flag_points()

        self.actors = arc.SpriteList()

        self.player = Player(scale=self.grid.scale)
        self.actors.append(self.player)

        self.spawn_player()

        self.physics_engine = arc.PhysicsEngineSimple(self.player, self.walls)

    def setup_maze(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = arc.get_window().get_size()

        x_span_diff = SCREEN_WIDTH - self.grid.width
        y_span_diff = SCREEN_HEIGHT - self.grid.height
        x_offset = (self.grid.real_block_size + x_span_diff) / 2
        y_offset = (self.grid.real_block_size + y_span_diff) / 2
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                center_x = (x * self.grid.real_block_size) + x_offset
                center_y = (y * self.grid.real_block_size) + y_offset
                block: arc.Sprite
                if col == BlockType.WALL:
                    block = arc.Sprite(TEXTURE_WALL, self.grid.scale)
                    self.walls.append(block)
                elif col == BlockType.PATH:
                    block = arc.Sprite(TEXTURE_PATH, self.grid.scale)
                    self.path.append(block)
                block.center_x, block.center_y = center_x, center_y

    def spawn_player(self):
        self.player.center_x, self.player.center_y = self.grid.center_of(
            *self.grid.start_point()
        )

    def set_flag_points(self):
        self.flag_start.center_x, self.flag_start.center_y = self.grid.center_of(
            *self.grid.start_point()
        )
        self.flag_stop.center_x, self.flag_stop.center_y = self.grid.center_of(
            *self.grid.stop_point()
        )

    def on_draw(self):
        self.clear()

        self.walls.draw()
        self.path.draw()
        self.flags.draw()
        self.actors.draw()

    def on_update(self, delta_time):
        self.actors.update()
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arc.key.UP:
            self.player.move_up()
        elif key == arc.key.DOWN:
            self.player.move_down()
        elif key == arc.key.LEFT:
            self.player.move_left()
        elif key == arc.key.RIGHT:
            self.player.move_right()
        elif key == arc.key.R:
            self.setup()

    def on_key_release(self, key, modifiers):
        if key == arc.key.UP or key == arc.key.DOWN:
            self.player.change_y = 0
        elif key == arc.key.LEFT or key == arc.key.RIGHT:
            self.player.change_x = 0

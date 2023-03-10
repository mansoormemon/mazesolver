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

TANK_BLUE = ":resources:images/topdown_tanks/tank_blue.png"
TANK_RED = ":resources:images/topdown_tanks/tank_red.png"


PLAYER_1_NAME = "Blue"
PLAYER_2_NAME = "Red"

PLAYER_SPEED = 2


class BlockType:
    WALL = 0
    PATH = 1


class View(arc.View):
    def __init__(self, window=None):
        super().__init__(window)

        self.active = None
        self.enable_help = None
        self.bot_previous_coords = None

        self.maze = None
        self.grid = None

        self.walls = None
        self.path = None

        self.flags = None
        self.flag_start = None
        self.flag_stop = None

        self.actors = None
        self.player_1 = None
        self.player_2 = None

        self.physics_engine_1 = None
        self.physics_engine_2 = None

        self.win_label = None

    def setup(self):
        arc.set_background_color(arc.color.ALMOND)

        self.active = True
        self.enable_help = False

        self.maze = Maze.generate(RAW_MAZE_SHAPE, seed=int(time.time()))
        self.solution = Maze.solve(self.maze)
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

        self.player_1 = Player(
            PLAYER_1_NAME, TANK_BLUE, PLAYER_SPEED, scale=self.grid.scale
        )
        self.actors.append(self.player_1)
        self.player_2 = Player(
            PLAYER_2_NAME, TANK_RED, PLAYER_SPEED, scale=self.grid.scale
        )
        self.actors.append(self.player_2)

        self.spawn_actors()

        self.physics_engine_1 = arc.PhysicsEngineSimple(self.player_1, self.walls)
        self.physics_engine_2 = arc.PhysicsEngineSimple(self.player_2, self.walls)

        self.win_label = None

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

    def spawn_actors(self):
        self.player_1.move_to(self.grid.center_of(*self.grid.start_point()))
        self.player_2.move_to(self.grid.center_of(*self.grid.start_point()))

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

        if self.enable_help:
            for r, row in enumerate(self.solution):
                for c, col in enumerate(row):
                    if col:
                        arc.draw_point(*self.grid.center_of(r, c), arc.color.RED, 3)

        self.actors.draw()
        if self.win_label is not None:
            self.win_label.draw()

    def on_update(self, delta_time):
        if self.active:
            SCREEN_WIDTH, SCREEN_HEIGHT = arc.get_window().get_size()
            self.actors.update()
            self.physics_engine_1.update()
            self.physics_engine_2.update()

            collisions = arc.check_for_collision_with_list(self.flag_stop, self.actors)
            if collisions:
                winner, *_ = collisions
                self.active = False
                winner.move_to(self.grid.center_of(*self.grid.stop_point()))
                self.win_label = arc.Text(
                    f"{winner.name} won!",
                    start_x=SCREEN_WIDTH / 2,
                    start_y=SCREEN_HEIGHT * 0.95,
                    anchor_x="center",
                    anchor_y="center",
                    font_name="Kenney Mini Square",
                    font_size=32,
                    color=arc.color.WINE_DREGS,
                )

    def on_key_press(self, key, modifiers):
        if key == arc.key.UP:
            self.player_1.move_up()
        elif key == arc.key.DOWN:
            self.player_1.move_down()
        elif key == arc.key.LEFT:
            self.player_1.move_left()
        elif key == arc.key.RIGHT:
            self.player_1.move_right()
        elif key == arc.key.R:
            self.setup()
        elif key == arc.key.H:
            self.enable_help = True
        elif key == arc.key.A:
            self.player_2.move_left()
        elif key == arc.key.D:
            self.player_2.move_right()
        elif key == arc.key.W:
            self.player_2.move_up()
        elif key == arc.key.S:
            self.player_2.move_down()

    def on_key_release(self, key, modifiers):
        if key == arc.key.UP or key == arc.key.DOWN:
            self.player_1.change_y = 0
        elif key == arc.key.LEFT or key == arc.key.RIGHT:
            self.player_1.change_x = 0
        elif key == arc.key.H:
            self.enable_help = False
        elif key == arc.key.A or key == arc.key.D:
            self.player_2.change_x = 0
        elif key == arc.key.W or key == arc.key.S:
            self.player_2.change_y = 0

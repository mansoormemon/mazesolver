import arcade as arc


class Grid:
    def __init__(self, shape, block_size, scale):
        SCREEN_WIDTH, SCREEN_HEIGHT = arc.get_window().get_size()

        self.shape = shape
        self.block_size = block_size
        self.scale = scale

        self.rows, self.columns = shape
        self.real_block_size = block_size * scale
        self.height, self.width = (self.real_block_size * mag for mag in self.shape)

        self.begin = (SCREEN_WIDTH - self.width) / 2, (SCREEN_HEIGHT + self.height) / 2

    def x_tiles(self):
        return self.columns

    def y_tiles(self):
        return self.rows

    def center_of(self, r, c):
        begin_x, begin_y = self.begin
        center_x = begin_x + (c * self.real_block_size) + (self.real_block_size / 2)
        center_y = begin_y - (r * self.real_block_size) - (self.real_block_size / 2)
        return center_x, center_y

    def start_point(self):
        return 1, 1

    def stop_point(self):
        return (mag - 2 for mag in self.shape)

    def get_location(self, x, y):
        begin_x, begin_y = self.begin
        return begin_x + (self.real_block_size * (x + 0.5)), begin_y - (
            self.real_block_size * (y + 0.5)
        )

    def get_coords(self, x, y):
        begin_x, begin_y = self.begin
        dx, dy = x - begin_x, begin_y - y
        return int(dx // self.real_block_size), int(dy // self.real_block_size)

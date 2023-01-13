import arcade as arc

from view import View

WINDOW_WIDTH, WINDOW_HEIGHT = 1440, 896
WINDOW_TITLE = "Maze Solver"


class Simulation(arc.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, *args, **kwargs)

    def setup(self):
        view = View()
        view.setup()
        self.show_view(view)

import arcade as arc


MOVEMENT_SPEED = 2


FACE_UP = 180
FACE_DOWN = 0
FACE_LEFT = 270
FACE_RIGHT = 90


class Player(arc.Sprite):
    def __init__(self, skin, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.texture = arc.load_texture(skin)
        self.textures.append(self.texture)

    def move_to(self, coords):
        self.center_x, self.center_y = coords

    def move_up(self):
        self.change_y = MOVEMENT_SPEED
        self.angle = FACE_UP

    def move_down(self):
        self.change_y = -MOVEMENT_SPEED
        self.angle = FACE_DOWN

    def move_left(self):
        self.change_x = -MOVEMENT_SPEED
        self.angle = FACE_LEFT

    def move_right(self):
        self.change_x = MOVEMENT_SPEED
        self.angle = FACE_RIGHT

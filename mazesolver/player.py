import arcade as arc


PLAYER_SKIN = (
    ":resources:images/topdown_tanks/tank_blue.png"
)
MOVEMENT_SPEED = 2


class TextureTypeList:
    LEFT_FACE = 0
    RIGHT_FACE = 1


class Player(arc.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.textures = arc.load_texture_pair(PLAYER_SKIN)
        self.set_texture(TextureTypeList.LEFT_FACE)

    def move_up(self):
        self.change_y = MOVEMENT_SPEED

    def move_down(self):
        self.change_y = -MOVEMENT_SPEED

    def move_left(self):
        self.change_x = -MOVEMENT_SPEED
        self.set_texture(TextureTypeList.LEFT_FACE)

    def move_right(self):
        self.change_x = MOVEMENT_SPEED
        self.set_texture(TextureTypeList.RIGHT_FACE)

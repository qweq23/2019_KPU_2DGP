from pico2d import *

import framework

TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

LOGO_POSITION_X = 800 / 2
LOGO_POSITION_Y = 500


class GameLogo:
    def __init__(self):
        self.images = [load_image('Image/title_Galaga0.png'), load_image('Image/title_Galaga1.png'),
                       load_image('Image/title_Galaga2.png'), load_image('Image/title_Galaga3.png'),
                       load_image('Image/title_Galaga4.png'), load_image('Image/title_Galaga3.png'),
                       load_image('Image/title_Galaga2.png'), load_image('Image/title_Galaga1.png')]
        self.frame = 0

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 8

    def draw(self):
        self.images[int(self.frame)].draw(LOGO_POSITION_X, LOGO_POSITION_Y)

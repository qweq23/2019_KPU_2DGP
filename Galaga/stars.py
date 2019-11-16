from pico2d import *

import framework
import gameworld

# 움직임 없음

FRONT_STARS_SPEED_PPS = 300

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2


class BG_Stars:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.front_stars_image = [load_image('Image/background_front1.png'),
                                  load_image('Image/background_front2.png')]
        self.front_stars_frame = 0
        gameworld.add_object(self, 0)

    def update(self):
        self.front_stars_frame = \
            (self.front_stars_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 2

    def draw(self):
        self.front_stars_image[int(self.front_stars_frame)].draw(self.x, self.y)


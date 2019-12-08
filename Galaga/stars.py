from pico2d import *

import framework

# 움직임 없음

FRONT_STARS_SPEED_PPS = 300

TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

STARS_SPEED_PPS = 150


class BG_Stars:
    def __init__(self, x, y):
        self.drawing_pos_x, self.drawing_pos_y = x, y
        self.bottom_pos_x = 0
        self.front_stars_image = [load_image('Image/background_front1.png'),
                                  load_image('Image/background_front2.png')]
        self.front_stars_frame = 0

    def update(self):
        self.front_stars_frame = \
            (self.front_stars_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 2
        self.bottom_pos_x = (self.bottom_pos_x + (STARS_SPEED_PPS * framework.frame_time)) % 800

    def draw(self):
        self.front_stars_image[int(self.front_stars_frame)].clip_draw(
            0, int(self.bottom_pos_x), 600, 800, self.drawing_pos_x, self.drawing_pos_y)


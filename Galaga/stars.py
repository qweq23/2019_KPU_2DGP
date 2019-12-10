from pico2d import *

import framework

FRONT_STARS_SPEED_PPS = 180
BACK_STARS_SPEED_PPS = 90

TIME_PER_FRONT_ACTION = 1.1
FRONT_ACTION_PER_TIME = 1.0 / TIME_PER_FRONT_ACTION
FRAMES_PER_FRONT_ACTION = 2

TIME_PER_BACK_ACTION = 1.3
BACK_ACTION_PER_TIME = 1.0 / TIME_PER_BACK_ACTION
FRAMES_PER_BACK_ACTION = 2


class Stars:
    def __init__(self, x, y):
        self.drawing_pos_x, self.drawing_pos_y = x, y
        self.front_stars_bottom_pos = 400
        self.back_stars_bottom_pos = 0

        self.front_stars_image = [load_image('Image/front_stars1.png'),
                                  load_image('Image/front_stars2.png')]
        self.back_stars_image = [load_image('Image/back_stars1.png'),
                                 load_image('Image/back_stars2.png')]

        self.front_stars_frame = 0
        self.back_stars_frame = 0

        self.moving = False

    def update(self):
        self.front_stars_frame = \
            (self.front_stars_frame + FRAMES_PER_FRONT_ACTION * FRONT_ACTION_PER_TIME * framework.frame_time) % 2
        self.back_stars_frame = \
            (self.back_stars_frame + FRAMES_PER_BACK_ACTION * BACK_ACTION_PER_TIME * framework.frame_time) % 2

        if self.moving:
            self.front_stars_bottom_pos = \
                (self.front_stars_bottom_pos + (FRONT_STARS_SPEED_PPS * framework.frame_time)) % 800
            self.back_stars_bottom_pos = \
                (self.back_stars_bottom_pos + (BACK_STARS_SPEED_PPS * framework.frame_time)) % 800

    def draw(self):
        self.front_stars_image[int(self.front_stars_frame)].clip_draw(
            0, int(self.front_stars_bottom_pos), 600, 800, self.drawing_pos_x, self.drawing_pos_y)
        self.back_stars_image[int(self.back_stars_frame)].clip_draw(
            0, int(self.back_stars_bottom_pos), 600, 800, self.drawing_pos_x, self.drawing_pos_y)

    def move(self):
        self.moving = True

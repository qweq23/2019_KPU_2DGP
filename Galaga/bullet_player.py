from pico2d import *

import framework

BULLET_SPEED_PPS = 700

class Bullet:
    image = None

    def __init__(self, x):
        self.x, self.y = x, 72
        if Bullet.image is None:
            Bullet.image = load_image('Image/player_bullet_9.png')

    def get_bb(self):
        return self.x - 5, self.y - 10, self.x + 5, self.y + 10

    def update(self):
        self.y += BULLET_SPEED_PPS * framework.frame_time

    def draw(self):
        self.image.draw(self.x, self.y, 20, 20)
        # draw_rectangle(*self.get_bb())
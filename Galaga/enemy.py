from pico2d import *
import random

import framework
import gameworld


ACTION_PER_TIME = 2.0
FRAMES_PER_ACTION = 2

TIME_PER_DYING_ACTION = 0.5
DYING_ACTION_PER_TIME = 1.0 / TIME_PER_DYING_ACTION
FRAMES_PER_DYING_ACTION = 5

class Enemy:
    dead_image = None

    def __init__(self, x, y):
        self.arrayed_x, self.arrayed_y = x, y

        if Enemy.dead_image is None:
            Enemy.dead_image = [load_image('Image/enemy_explosion0_39.png'),
                                load_image('Image/enemy_explosion1_39.png'),
                                load_image('Image/enemy_explosion2_39.png'),
                                load_image('Image/enemy_explosion3_39.png'),
                                load_image('Image/enemy_explosion4_39.png')]

    def update(self):
        pass

    def draw(self):
        pass


class Bee(Enemy):
    image = None

    def __init__(self, x, y):
        Enemy(x, y)
        self.cur_x, self.cur_y = x, y
        self.dying = False
        self.dying_timer = 0
        self.dying_frame = 0
        self.idle_frame = random.randint(0, 1 + 1)
        if Bee.image is None:
            Bee.image = load_image('Image/bee_sprite_34x17.png')

    def get_bb(self):
        return self.cur_x - 20, self.cur_y - 20, self.cur_x + 20, self.cur_y + 20

    def die(self):
        self.dying = True
        self.dying_timer = TIME_PER_DYING_ACTION

    def update(self):
        if self.dying is False:
            self.idle_frame = (self.idle_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 2

        else:
            self.dying_timer -= framework.frame_time
            if self.dying_timer < 0:
                gameworld.remove_object(self)

            self.dying_frame = (self.dying_frame + FRAMES_PER_DYING_ACTION * DYING_ACTION_PER_TIME
                                * framework.frame_time) % 5

    def draw(self):
        if self.dying is False:
            Bee.image.clip_draw(int(self.idle_frame) * 17, 0, 17, 17,
                                self.cur_x, self.cur_y, 50, 50)
            # draw_rectangle(*self.get_bb())

        else:
            Enemy.dead_image[int(self.dying_frame)].draw(self.cur_x, self.cur_y, 50, 50)


class Butterfly(Enemy):
    image = None

    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        if Butterfly.image is None:
            Butterfly.image = load_image('Image/butterfly_sprite_34x17.png')


class Moth(Enemy):
    image = None

    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        if Moth.image is None:
            Moth.image = load_image('Image/moth_sprite_34.png')

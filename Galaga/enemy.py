from pico2d import *
import random

import framework
import gameworld

TIME_PER_FLYING_ACTION = 0.6
FLYING_ACTION_PER_TIME = 1.0 / TIME_PER_FLYING_ACTION
FRAMES_PER_FLYING_ACTION = 2

TIME_PER_EXPLODE_ACTION = 0.5
EXPLODE_ACTION_PER_TIME = 1.0 / TIME_PER_EXPLODE_ACTION
FRAMES_PER_EXPLODE_ACTION = 5

enemy_explode_images = []


def load_explode_images():
    global enemy_explode_images
    enemy_explode_images = [load_image('Image/enemy_explosion0_39.png'),
                            load_image('Image/enemy_explosion1_39.png'),
                            load_image('Image/enemy_explosion2_39.png'),
                            load_image('Image/enemy_explosion3_39.png'),
                            load_image('Image/enemy_explosion4_39.png')]
    print('로드됨')
    print(len(enemy_explode_images))

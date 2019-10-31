from pico2d import *
import random

import gameworld

# 적들의 3가지 상태
# 1. 등장 2. 정렬 3. 퇴장
# 적이 생성될 때 어느 위치에 정렬될 지 그 좌표값을 가지고 있어야 한다.


class Enemy:
    dead_image = None

    def __init__(self, x, y):
        self.arrayed_x, self.arrayed_y = x, y
        # self.cur_x, self.cur_y = None, None

        self.region_left = 0
        self.region_top = 0
        self.region_right = 0
        self.region_bottom = 0

        self.frame = 0
        if Enemy.dead_image == None:
            Enemy.dead_image = [load_image('Image/enemy_explosion0_39.png'),
                                load_image('Image/enemy_explosion1_39.png'),
                                load_image('Image/enemy_explosion2_39.png'),
                                load_image('Image/enemy_explosion3_39.png'),
                                load_image('Image/enemy_explosion4_39.png')]


    def update(self):
        # 위치 업데이트
        pass

    def draw(self):
        pass

    # 적은 스테이지가 진행되는 동안 정해진 시간에 정해진 위치에 있게 된다 즉, 동선이 정해져 있다


class Bee(Enemy):

    def __init__(self, x, y):
        Enemy(x, y)
        self.cur_x, self.cur_y = x, y
        self.frame = random.randint(0, 100)
        self.image = load_image('Image/bee_sprite_34x17.png')

    def update(self):
        self.frame = (self.frame + 1) % 200
        self.region_left = self.cur_x - 25
        self.region_top = self.cur_y + 25
        self.region_right = self.cur_x + 25
        self.region_bottom = self.cur_y - 20


    def draw(self):
        self.image.clip_draw(self.frame // 100 * 17, 0, 17, 17,
                             self.cur_x, self.cur_y, 50, 50)


class Butterfly(Enemy):
    pass


class Moth(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.hp = 2
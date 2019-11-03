from pico2d import *
import random

import gameworld

# 적들의 4가지 상태
# 1. 등장 2. 정렬 3. 퇴장 4. 죽음
# 적들은 한 스테이지에서 일정 시간에 일정한 위치에 있어야 한다.
# 적이 생성될 때 어느 위치에 정렬될 지 그 좌표값을 가지고 있어야 한다.


# 적 클래스: 적들의 죽는 스프라이트를 저장한다. 정렬될 위치를 초기화한다.
class Enemy:
    dead_image = None

    def __init__(self, x, y):
        self.arrayed_x, self.arrayed_y = x, y

        self.region_left = 0
        self.region_top = 0
        self.region_right = 0
        self.region_bottom = 0
        self.dying = False
        self.dying_frame = 0
        self.timer = 0
        self.frame = 0
        if Enemy.dead_image is None:
            Enemy.dead_image = [load_image('Image/enemy_explosion0_39.png'),
                                load_image('Image/enemy_explosion1_39.png'),
                                load_image('Image/enemy_explosion2_39.png'),
                                load_image('Image/enemy_explosion3_39.png'),
                                load_image('Image/enemy_explosion4_39.png')]

    def get_bb(self):
        return

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
        self.dying_frame = 0
        self.frame = random.randint(0, 100)
        if Bee.image is None:
            Bee.image = load_image('Image/bee_sprite_34x17.png')



    def update(self):
        self.frame = (self.frame + 1) % 200
        self.region_left = self.cur_x - 25
        self.region_top = self.cur_y + 25
        self.region_right = self.cur_x + 25
        self.region_bottom = self.cur_y - 20
        if self.dying is True:
            self.dying_frame = self.dying_frame + 1
            if self.dying_frame == 250:
                gameworld.remove_object(self)

    def draw(self):
        if self.dying is False:
            Bee.image.clip_draw(self.frame // 100 * 17, 0, 17, 17,
                                 self.cur_x, self.cur_y, 50, 50)
        else:
            Enemy.dead_image[self.dying_frame // 50].draw(self.cur_x, self.cur_y, 50, 50)



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


        self.hp = 2




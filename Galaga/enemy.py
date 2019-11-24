from pico2d import *
import random

import framework
import gameworld

# 적 스테이트 구상
# 1. 적이 등장할 때
# 2. 정렬되서 좌우로 움직임
# 3. 퇴장
# 적이 움직이는 건 어떤 스테이지에서 어떤 시간이냐에 따라서 달라진다.
# 그러면 적의 이동 경로는 스테이지가 가지고 있어야 하는 것 아닌가..?
# 그러면 적은 이동 경로의 다음 점을 입력 받아서 위치를 업데이트 하는 일만 하면 되는 건가


class ArriveState:
    pass


class StayState:
    pass


class LeaveState:
    pass


ACTION_PER_TIME = 2.0
FRAMES_PER_ACTION = 2

TIME_PER_DYING_ACTION = 0.5
DYING_ACTION_PER_TIME = 1.0 / TIME_PER_DYING_ACTION
FRAMES_PER_DYING_ACTION = 5


class Bee:
    image = None

    def __init__(self, x, y):
        self.arrayed_x , arrayed_y = x, y
        self.cur_x, self.cur_y = x, y
        self.dying = False
        self.dying_timer = 0
        self.dying_frame = 0
        self.idle_frame = 1 / random.randint(1, 100)
        if Bee.image is None:
            Bee.image = load_image('Image/bee_sprite_34x17.png')

        # 죽는 이미지 함수로 바꾸던가 해라
        self.dead_images = [load_image('Image/enemy_explosion0_39.png'),
                            load_image('Image/enemy_explosion1_39.png'),
                            load_image('Image/enemy_explosion2_39.png'),
                            load_image('Image/enemy_explosion3_39.png'),
                            load_image('Image/enemy_explosion4_39.png')]

        gameworld.add_object(self, 1)

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
            self.dead_images[int(self.dying_frame)].draw(self.cur_x, self.cur_y, 50, 50)


# 정렬된 상태일 때만 플레이어의 총알을 튕기도록 구현한다
class Butterfly:
    image = None

    def __init__(self, x, y):
        self.arrayed_x, arrayed_y = x, y
        self.cur_x, cur_y = x, y
        if Butterfly.image is None:
            Butterfly.image = load_image('Image/butterfly_sprite_34x17.png')


class Moth:
    image = None

    def __init__(self, x, y):
        self.arrayed_x, arrayed_y = x, y
        self.cur_x, cur_y = x, y
        if Moth.image is None:
            Moth.image = load_image('Image/moth_sprite_34.png')

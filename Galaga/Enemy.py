from pico2d import *

# 적들의 3가지 상태
# 1. 등장 2. 정렬 3. 퇴장
# 적이 생성될 때 어느 위치에 정렬될 지 그 좌표값을 가지고 있어야 한다.

class Enemy:
    image = None

    def __init__(self, x, y):
        self.arrayed_x, self.arrayed_y = x, y
        self.cur_x, self.cur_y = None, None
        if Enemy.image == None:
            Enemy.image = load_image('Image/enemy_sprite_37x68.png')

    def update(self):
        # 위치 업데이트
        pass

    def draw(self):
        pass

    # 적은 스테이지가 진행되는 동안 정해진 시간에 정해진 위치에 있게 된다 즉, 동선이 정해져 있다


class Bee(Enemy):
    pass


class Butterfly(Enemy):
    pass


class Moth(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.hp = 2


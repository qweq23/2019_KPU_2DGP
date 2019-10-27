from Galaga.Global import *
import Bullet


class Player:
    def __init__(self):
        # 플레이어
        self.x, self.y = CONST_CLIENT_WIDTH / 2, CONST_PLAYER_Y
        self.life = 3
        self.frame = 0;

        # 이미지 로드
        self.image = load_image('./Image/player_17.png')  # 플레이어 이미지 로드하기
        self.dying_image = [load_image("./Image/explosion0_39.png"),
                            load_image("./Image/explosion1_39.png"),
                            load_image("./Image/explosion2_39.png"),
                            load_image("./Image/explosion3_39.png")]

    def draw(self):
        self.image.draw(self.x, self.y)
        pass

    def move(self, dir):
        # 방향을 받아와서 움직임
        pass

    def shoot(self):
        # 플레이어의 현제 위치에서 총알을 생성한다.
        pass
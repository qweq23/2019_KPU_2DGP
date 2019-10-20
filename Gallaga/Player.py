from Global import *

class Player:
    def __init__(self):
        # 플레이어 초기 위치
        self.x = client_w / 2
        self.life = 3
        self.image = load_image()  # 플레이어 이미지 로드하기
        self.dying_image = load_image()  # 플레이어 죽는 스프라이트

    def draw(self):
        # 평소 모습
        # 죽을 때
        pass

    def move(self):
        pass


from pico2d import *

import gameworld

PLAYER_POSITION_Y = 50
PLAYER_SIZE = 50
PLAYER_SPEED = 1


class Player:
    def __init__(self):
        self.x, self.y = 300, PLAYER_POSITION_Y
        self.image = load_image('Image/player_17.png')
        self.velocity = 0

    def shoot(self):
        # 게임 월드에 bullet 오브젝트를 추가한다.
        pass

    def control(self, event_type, event_key):
        # 이동, 공격
        if event_type == SDL_KEYDOWN:
            if event_key == SDLK_RIGHT:
                self.velocity += PLAYER_SPEED
            elif event_key == SDLK_LEFT:
                self.velocity -= PLAYER_SPEED
            elif event_key == SDLK_SPACE:
                self.shoot()

        elif event_type == SDL_KEYUP:
            if event_key == SDLK_RIGHT:
                self.velocity -= PLAYER_SPEED
            elif event_key == SDLK_LEFT:
                self.velocity += PLAYER_SPEED
            elif event_key == SDLK_SPACE:
                pass



    def update_position(self):
        next_position = self.x + self.velocity
        if next_position > 25 and next_position < 575:
            self.x = next_position



    def draw(self):
        self.image.draw(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)


class Bullet:
    image = None

    def __init__(self, x):
        self.x, self.y = x, PLAYER_POSITION_Y
        if Bullet.image == None:
            Bullet.image = load_image('Image/player_bullet_9.png')

    def update_position(self):
        self.y += 2

    def draw(self):
        self.image.draw(self.x, self.y, 10, 10)

    def detect_collision(self):
        if self.y > 800:
            pass

        # 적에 맞았나 충돌체크는 어떻게..?
        # 게임 오브젝트들이 놓여있고, 서로 상호작용 하는 공간이 필요하다...!
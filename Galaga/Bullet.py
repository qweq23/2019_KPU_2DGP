from Global import *

# bullet list가 있어야하는데 어디..?


class PlayerBullet:
    def __init__(self, init_xPos):
        self.x, self.y = init_xPos, CONST_PLAYER_Y
        self.image = load_image("./image/player_bullet_9.png")


class EnemyBullet:
    def __init__(self):
        pass


if __name__ == '__main__':
    print("a")
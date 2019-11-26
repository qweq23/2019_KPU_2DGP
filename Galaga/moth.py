from enemy import *

# 초록 -> 파랑 -> 폭발


class GreenState:
    @staticmethod
    def enter(bee):
        pass

    @staticmethod
    def exit(bee):
        pass

    @staticmethod
    def do(bee):
        bee.flying_frame = (bee.flying_frame + FRAMES_PER_FLYING_ACTION * FLYING_ACTION_PER_TIME
                            * framework.frame_time) % FRAMES_PER_FLYING_ACTION

    @staticmethod
    def draw(bee):
        bee.image.clip_draw(int(bee.flying_frame) * 17, 17, 17, 17,
                            bee.x, bee.y, 50, 50)


class BlueState:
    @staticmethod
    def enter(bee):
        pass

    @staticmethod
    def exit(bee):
        pass

    @staticmethod
    def do(bee):
        bee.flying_frame = (bee.flying_frame + FRAMES_PER_FLYING_ACTION * FLYING_ACTION_PER_TIME
                            * framework.frame_time) % FRAMES_PER_FLYING_ACTION

    @staticmethod
    def draw(bee):
        bee.image.clip_draw(int(bee.flying_frame) * 17, 0, 17, 17,
                            bee.x, bee.y, 50, 50)


class ExplodeState:
    @staticmethod
    def enter(bee):
        bee.explode_timer = TIME_PER_EXPLODE_ACTION

    @staticmethod
    def exit(bee):
        gameworld.remove_object(bee)
        del bee

    @staticmethod
    def do(bee):
        bee.explode_timer -= framework.frame_time
        bee.explode_frame = (bee.explode_frame + FRAMES_PER_EXPLODE_ACTION * EXPLODE_ACTION_PER_TIME
                             * framework.frame_time) % FRAMES_PER_EXPLODE_ACTION
        if bee.explode_timer < 0:
            bee.cur_state.exit(bee)

    @staticmethod
    def draw(bee):
        bee.explode_images[int(bee.explode_frame)].draw(bee.x, bee.y, 75, 75)


class Moth:
    image = None

    def __init__(self, sorting_number, x, y):
        if Moth.image is None:
            Moth.image = load_image('Image/moth_sprite_34.png')

        # 이거 해결하세요
        self.explode_images = [load_image('Image/enemy_explosion0_39.png'),
                               load_image('Image/enemy_explosion1_39.png'),
                               load_image('Image/enemy_explosion2_39.png'),
                               load_image('Image/enemy_explosion3_39.png'),
                               load_image('Image/enemy_explosion4_39.png')]

        self.sorting_number = sorting_number
        self.x, self.y = x, y

        self.explode_timer = 0

        self.flying_frame = 0
        self.explode_frame = 0

        self.cur_state = GreenState
        self.cur_state.enter(self)

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def is_explode(self):
        if self.cur_state == ExplodeState:
            return True
        return False

    def hit(self):
        self.cur_state.exit(self)

        if self.cur_state == GreenState:
            self.cur_state = BlueState
        elif self.cur_state == BlueState:
            self.cur_state = ExplodeState

        self.cur_state.enter(self)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
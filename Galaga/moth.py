from enemy import *

import state_StageMain

MOVE_TIME = 2
MOVE_SPEED_PPS = 100


class GreenState:
    @staticmethod
    def enter(bee):
        pass

    @staticmethod
    def exit(bee):
        bee.chang_color_sound.play()

    @staticmethod
    def do(bee):
        bee.flying_frame = (bee.flying_frame + FRAMES_PER_FLYING_ACTION * FLYING_ACTION_PER_TIME
                            * framework.frame_time) % FRAMES_PER_FLYING_ACTION

        bee.x += MOVE_SPEED_PPS * bee.dir * framework.frame_time

        bee.move_timer -= framework.frame_time
        if bee.move_timer < 0:
            bee.dir = -bee.dir
            bee.move_timer = MOVE_TIME


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
        bee.dying_sound.play()

    @staticmethod
    def do(bee):
        bee.flying_frame = (bee.flying_frame + FRAMES_PER_FLYING_ACTION * FLYING_ACTION_PER_TIME
                            * framework.frame_time) % FRAMES_PER_FLYING_ACTION

        bee.x += MOVE_SPEED_PPS * bee.dir * framework.frame_time

        bee.move_timer -= framework.frame_time
        if bee.move_timer < 0:
            bee.dir = -bee.dir
            bee.move_timer = MOVE_TIME

    @staticmethod
    def draw(bee):
        bee.image.clip_draw(int(bee.flying_frame) * 17, 0, 17, 17,
                            bee.x, bee.y, 50, 50)


class ExplodeState:
    @staticmethod
    def enter(bee):
        bee.explode_timer = TIME_PER_EXPLODE_ACTION
        state_StageMain.enemies.remove(bee)

    @staticmethod
    def exit(bee):
        gameworld.remove_object(bee)

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


next_state_table = {
    GreenState: BlueState,
    BlueState: ExplodeState,
}


class Moth:
    image = None
    explode_images = None

    def __init__(self, coord_pos):
        if Moth.image is None:
            Moth.image = load_image('Image/moth_sprite_34.png')

        if Moth.explode_images is None:
            Moth.explode_images = [load_image('Image/enemy_explosion0_39.png'),
                                   load_image('Image/enemy_explosion1_39.png'),
                                   load_image('Image/enemy_explosion2_39.png'),
                                   load_image('Image/enemy_explosion3_39.png'),
                                   load_image('Image/enemy_explosion4_39.png')]

        self.move_timer = 1
        self.speed = MOVE_SPEED_PPS
        self.dir = 1
        self.x, self.y = coord_pos[0], coord_pos[1]

        self.explode_timer = 0

        self.flying_frame = 0
        self.explode_frame = 0

        self.cur_state = GreenState
        self.cur_state.enter(self)

        self.chang_color_sound = load_wav('Sound/MothChangeColor.wav')
        self.dying_sound = load_wav('Sound/MothDie.wav')
        self.attacking = False

    def is_attack_state(self):
        return False

    def attack(self, starship_pos):
        pass

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def hit(self):
        self.cur_state.exit(self)
        self.cur_state = next_state_table[self.cur_state]
        self.cur_state.enter(self)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)

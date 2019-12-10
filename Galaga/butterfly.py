from enemy import *
import random
from bullet_enemy import EnemyBullet

import state_StageMain


class IdleState:
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


class Butterfly:
    image = None
    explode_images = None

    def __init__(self, coord_pos):
        if Butterfly.image is None:
            Butterfly.image = load_image('Image/butterfly_sprite_34x17.png')

        if Butterfly.explode_images is None:
            Butterfly.explode_images = [load_image('Image/enemy_explosion0_39.png'),
                                        load_image('Image/enemy_explosion1_39.png'),
                                        load_image('Image/enemy_explosion2_39.png'),
                                        load_image('Image/enemy_explosion3_39.png'),
                                        load_image('Image/enemy_explosion4_39.png')]

        self.x, self.y = coord_pos[0], coord_pos[1]

        self.explode_timer = 0

        self.flying_frame = 0
        self.explode_frame = 0

        self.cur_state = IdleState
        self.cur_state.enter(self)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def shoot(self):
        bullet = EnemyBullet(self.x, self.y - 25)
        gameworld.add_object(bullet, 1)
        state_StageMain.enemy_bullets.append(bullet)

    def is_explode(self):
        if self.cur_state == ExplodeState:
            return True
        return False

    def hit(self):
        if random.randint(0, 1) == 0:
            self.shoot()

        self.cur_state.exit(self)
        self.cur_state = ExplodeState
        self.cur_state.enter(self)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

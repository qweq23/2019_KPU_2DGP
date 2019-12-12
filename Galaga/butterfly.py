from enemy import *
import random
from bullet_enemy import EnemyBullet
from BehaviorTree import BehaviorTree, LeafNode, SelectorNode, SequenceNode


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
        bee.image.clip_draw(int(bee.flying_frame) * 17, 0, 17, 17, bee.x, bee.y, 50, 50)


class ExplodeState:
    @staticmethod
    def enter(bee):
        bee.hit_sound.play()
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


class AttackState:
    @staticmethod
    def enter(bee):
        bee.attacking = True
        bee.attack_sound.play()

    @staticmethod
    def exit(bee):
        bee.attacking = False

    @staticmethod
    def do(bee):
        bee.attack_bt.run()

    @staticmethod
    def draw(bee):
        bee.image.clip_composite_draw(int(bee.flying_frame) * 17, 0, 17, 17,
                                      bee.dir + math.radians(-90), 'h', bee.x, bee.y, 50, 50)


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

        self.speed = 0
        self.dir = 0
        self.x, self.y = coord_pos
        self.target_pos = []

        self.explode_timer = 0

        self.flying_frame = 0
        self.explode_frame = 0

        self.cur_state = IdleState
        self.cur_state.enter(self)

        self.hit_sound = load_wav('Sound/ButterflyDie.wav')
        self.hit_sound.set_volume(256)
        self.attack_sound = load_wav('Sound/Attack.wav')

        self.attacking = False
        self.attack_positions = []
        self.attack_order = 0
        self.attack_bt = None
        self.build_behavior_tree()

    def is_attack_state(self):
        if self.cur_state == AttackState:
            return True
        else:
            return False

    def calculate_current_position(self):
        self.flying_frame = (self.flying_frame + FRAMES_PER_FLYING_ACTION * FLYING_ACTION_PER_TIME
                             * framework.frame_time) % FRAMES_PER_FLYING_ACTION
        self.x += self.speed * math.cos(self.dir) * framework.frame_time
        self.y += self.speed * math.sin(self.dir) * framework.frame_time

    def get_next_position(self):
        self.target_pos = self.attack_positions[self.attack_order % 2]
        self.attack_order += 1
        if self.attack_order == 3:
            self.x, self.y = self.attack_positions[1]
            self.attack_order = 0
            self.cur_state.exit(self)
            self.cur_state = IdleState
            self.cur_state.enter(self)
            return BehaviorTree.FAIL

        self.dir = math.atan2(self.target_pos[1] - self.y, self.target_pos[0] - self.x)
        return BehaviorTree.SUCCESS

    def move_to_target(self):
        self.speed = ATTACK_SPEED_PPS
        self.calculate_current_position()
        distance = (self.target_pos[0] - self.x) ** 2 + (self.target_pos[1] - self.y) ** 2
        if distance < 10 ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_attack_position(self):
        self.attack_positions = [(self.target_pos[0], self.target_pos[1]), (self.x, self.y)]

    def attack(self, starship_pos):
        self.target_pos = starship_pos
        self.set_attack_position()

        self.cur_state.exit(self)
        self.cur_state = AttackState
        self.cur_state.enter(self)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def shoot(self):
        bullet = EnemyBullet(self.x, self.y - 25)
        gameworld.add_object(bullet, 1)
        state_StageMain.enemy_bullets.append(bullet)

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

    def build_behavior_tree(self):
        attack_node = SequenceNode('Attack')
        get_next_position_node = LeafNode('Get Next Position', self.get_next_position)
        move_to_target_node = LeafNode('Move To Target', self.move_to_target)
        attack_node.add_children(get_next_position_node, move_to_target_node)
        self.attack_bt = BehaviorTree(attack_node)


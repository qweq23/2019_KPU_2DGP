from pico2d import *

import framework
import gameworld

starship_bullets = []
enemy_bullets = []

from starship import StarShip
from enemy import *

# 스테이트 바꾸는걸 어떻게 할까
ENTER_READY, READY_RUN, RUN_READY, RUN_EXIT, EXIT_ENTER = range(5)

READY_TIME = 2  # 3
ENTER_TIME = 1  # 3
EXIT_TIME = 2

# stage_number: enemies_list
stage_enemies_table = {
    1: []
}

# event type: (EVENT, VALUE)
LIFE, STAGE, SCORE = range(3)

LAST_STAGE = 5


class EnterState:
    @staticmethod
    def enter(stage):
        stage.enter_timer = ENTER_TIME

    @staticmethod
    def exit(stage):
        pass

    @staticmethod
    def do(stage):
        stage.enter_timer -= framework.frame_time
        if stage.enter_timer < 0:
            stage.update_state()

    @staticmethod
    def draw(stage):
        stage.font.draw(250, 400, 'stage %d' % stage.stage_number, (251, 100, 0))


class ReadyState:
    @staticmethod
    def enter(stage):
        stage.ready_timer = READY_TIME

    @staticmethod
    def exit(stage):
        if stage.starship is None:
            stage.create_starship()

    @staticmethod
    def do(stage):
        stage.ready_timer -= framework.frame_time
        if stage.ready_timer < 0:
            stage.update_state()


    @staticmethod
    def draw(stage):
        if stage.ready_timer < READY_TIME - 1:
            stage.font.draw(250, 400, 'Ready', (251, 100, 0))


class RunState:
    @staticmethod
    def enter(stage):
        stage.enemies = [Bee(100, 600), Bee(200, 600), Bee(300, 600),
                         Bee(400, 600), Bee(500, 600)]

    @staticmethod
    def exit(stage):
         # stage.delete_starship()
        pass

    @staticmethod
    def do(stage):
        if len(stage.enemies) == 0:
            stage.update_state()

        for enemy in stage.enemies:
            for bullet in starship_bullets:
                if intersect_bb(enemy, bullet):
                    stage.enemies.remove(enemy)
                    enemy.die()
                    starship_bullets.remove(bullet)
                    gameworld.remove_object(bullet)

        for enemy in stage.enemies:
            if intersect_bb(stage.starship, enemy):
                stage.die_starship()
                stage.enemies.remove(enemy)
                enemy.die()
                break

    @staticmethod
    def draw(stage):
        pass


class ExitState:
    @staticmethod
    def enter(stage):
        stage.exit_timer = EXIT_TIME

    @staticmethod
    def exit(stage):
        if stage.stage_number == LAST_STAGE:
            framework.quit()


    @staticmethod
    def do(stage):
        stage.exit_timer -= framework.frame_time
        if stage.exit_timer < 0:
            stage.update_state()

    @staticmethod
    def draw(stage):
        stage.font.draw(250, 400, 'EXIT', (251, 100, 0))


stage_loop_table = {
    EnterState: ReadyState,
    ReadyState: RunState,
    RunState: ExitState,
    ExitState: EnterState
}

class Stage:
    def __init__(self):
        # event type: (EVENT, VALUE)
        self.ui_event_que = []

        self.stage_number = 1
        self.stage_timer = 0  # sec
        self.cur_state = EnterState
        self.cur_state.enter(self)

        self.enter_timer = ENTER_TIME
        self.ready_timer = READY_TIME
        self.exit_timer = EXIT_TIME

        self.run_timer = 0

        self.starship = None
        self.enemies = []

        self.font = load_font('Font/LCD_Solid.ttf', 24)

        gameworld.add_object(self, 1)

    def create_starship(self):
        self.starship = StarShip()

    def delete_starship(self):
        self.starship.die()
        self.starship = None

    def die_starship(self):
        self.delete_starship()
        self.cur_state.exit(self)
        self.cur_state = ReadyState
        self.cur_state.enter(self)

    def put_ui_event(self):
        if len(self.ui_event_que) == 0:
            return None
        else:
            event = self.ui_event_que[0]
            self.ui_event_que.remove(event)
            return event

    def update_state(self):
        self.cur_state.exit(self)
        self.cur_state = stage_loop_table[self.cur_state]
        if self.cur_state == EnterState:
            self.stage_number += 1
            self.ui_event_que.append((STAGE, 1))
        self.cur_state.enter(self)


    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if self.starship is not None:
            self.starship.handle_event(event)


def intersect_bb(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

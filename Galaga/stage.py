from pico2d import *

import framework
import gameworld

from starship import StarShip
from enemy import *

# 화면 중앙에 ready 뜨는 것도 스테이지에서 해야할 일 같다...
# 플레이어가 죽었을 때, 게임 스테이지 진행에 영향을 미치는가?
# 플레이어가 죽으면 퇴장하던 적이 다시 정렬 위치로 올라간다. -> 이거 구현 할거냐
# 정렬된 상태면 적들의 정렬 상태가 변한다 -> 이것도 구현 할거냐...
# 적이 등장할 때는 플레이어가 죽을 일이 없다


# stage_number: enemies_list
stage_enemies_table = {
    1: []
}

# stage_number: stage_time
stage_time_table = {
    1: 5,
    2: 5,
    3: 5,
    4: 5,
    5: 5,
}

# event type: (EVENT, VALUE)
LIFE, STAGE, SCORE = range(3)


LAST_STAGE = 5


class EnterState:
    @staticmethod
    def enter(stage):
        stage.set_timer()

    @staticmethod
    def exit(stage):
        pass

    @staticmethod
    def do(stage):
        if stage_time_table[stage.stage_number] - stage.stage_timer > 2:
            stage.update_state()


    @staticmethod
    def draw(stage):
        stage.font.draw(280, 400, 'stage %d' % stage.stage_number, (251, 100, 0))


class RunState:
    @staticmethod
    def enter(stage):
        # 스테이지 넘버에 따라서 알맞은 적들의 리스트를 인스턴스해야 한다.
        # -> 매칭이 하고싶다 -> 테이블을 만들어라
        if stage.stage_number == 1:
            stage.starship = StarShip()

        stage.enemies = [Bee(100, 600), Bee(200, 600), Bee(300, 600),
                         Bee(400, 600), Bee(500, 600)]

    @staticmethod
    def exit(stage):
        pass

    @staticmethod
    def do(stage):
        if stage.stage_timer < 0:
            stage.update_state()

    @staticmethod
    def draw(stage):
        pass


class ExitState:
    @staticmethod
    def enter(stage):
        stage.update_state()

    @staticmethod
    def exit(stage):
        if stage.stage_number == 5:
            framework.quit()


    @staticmethod
    def do(stage):
        pass

    @staticmethod
    def draw(stage):
        pass


stage_loop_table = {
    EnterState: RunState,
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

        self.starship = None
        self.enemies = []

        self.font = load_font('Font/LCD_Solid.ttf', 24)

        gameworld.add_object(self, 1)

    def set_timer(self):
        self.stage_timer = stage_time_table[self.stage_number]

    def update_state(self):
        self.cur_state.exit(self)
        self.cur_state = stage_loop_table[self.cur_state]
        if self.cur_state == EnterState:
            self.stage_number += 1
            self.ui_event_que.append((STAGE, 1))
        self.cur_state.enter(self)

    def update(self):
        self.stage_timer -= framework.frame_time
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if self.starship is not None:
            self.starship.handle_event(event)

    def put_ui_event(self):
        if len(self.ui_event_que) > 0:
            event = self.ui_event_que[0]
            self.ui_event_que.remove(event)
            return event
        return None

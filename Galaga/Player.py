from pico2d import *

import framework
import gameworld
from bullet_player import Bullet

RIGHT_DOWN, LEFT_DOWN, SPACE_DOWN, RIGHT_UP, LEFT_UP, SPACE_UP, DEAD_TIMER = range(7)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP,
}

class IdleState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity += PLAYER_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity -= PLAYER_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity -= PLAYER_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity += PLAYER_SPEED_PPS





    @staticmethod
    def exit(player, event):
        if event == SPACE_DOWN:
            gameworld.add_object(Bullet(player.x), 1)
    @staticmethod
    def do(player):
        player.x += player.velocity * framework.frame_time
        player.x = clamp(25, player.x, 600 - 25)

    @staticmethod
    def draw(player):
        player.image.draw(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)


class DeadState:
    @staticmethod
    def enter(player, event):
        pass

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass


class ReadyState:
    @staticmethod
    def enter(player, event):
        pass

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass


next_state_table = {
    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,
                SPACE_DOWN: IdleState, SPACE_UP: IdleState,
                DEAD_TIMER: DeadState},


    DeadState: {RIGHT_UP: DeadState, LEFT_UP: DeadState,
                RIGHT_DOWN: DeadState, LEFT_DOWN: DeadState,
                SPACE_DOWN: DeadState, SPACE_UP: DeadState,
                DEAD_TIMER: IdleState}
}


PLAYER_SIZE = 50
PLAYER_SPEED_PPS = 250


class Player:
    def __init__(self):
        self.x, self.y = 300, 50

        self.image = load_image('Image/player_17.png')
        self.dead_image = [load_image('Image/explosion0_39.png'), load_image('Image/explosion1_39.png'),
                           load_image('Image/explosion2_39.png'), load_image('Image/explosion3_39.png')]
        self.life = 3
        self.velocity = 0
        self.dead_frame = 0

        self.event_que = []

        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def get_bb(self):
        length_from_center = PLAYER_SIZE / 2
        return self.x - length_from_center, self.y - length_from_center, \
            self.x + length_from_center, self.y + length_from_center

    def update_state(self):
        # 이벤트 큐에 뭐가 있으면
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        self.update_state()

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if(event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)




from pico2d import *
import time

import framework
import gameworld
from bullet_player import PlayerBullet

RIGHT_DOWN, LEFT_DOWN, SPACE_DOWN, RIGHT_UP, LEFT_UP, SPACE_UP, DEAD_TIMER, READY_TIMER, RESPAWN_TIMER = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP,
}

PLAYER_SIZE = 50
PLAYER_SPEED_PPS = 250

TIME_PER_DYING_ACTION = 0.8
DYING_ACTION_PER_TIME = 1.0 / TIME_PER_DYING_ACTION
FRAMES_PER_DYING_ACTION = 4

class ReadyState:
    @staticmethod
    def enter(player, event):
        if event == READY_TIMER:
            player.ready_time = 2

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.ready_time -= framework.frame_time
        if player.ready_time < 0:
            player.add_event(READY_TIMER)

    @staticmethod
    def draw(player):
        framework.font.draw(280, 400, 'Ready', (251, 100, 0))


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
            gameworld.add_object(PlayerBullet(player.x), 1)

    @staticmethod
    def do(player):
        player.x += player.velocity * framework.frame_time
        player.x = clamp(25, player.x, 600 - 25)
        # player.add_event(DEAD_TIMER)

    @staticmethod
    def draw(player):
        player.starship_image.draw(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)


class DeadState:
    @staticmethod
    def enter(player, event):
        if event == DEAD_TIMER:
            player.life -= 1
            player.death_time = TIME_PER_DYING_ACTION

    @staticmethod
    def exit(player, event):
        player.dying_frame = 0

    @staticmethod
    def do(player):
        player.dying_frame = (player.dying_frame + FRAMES_PER_DYING_ACTION * DYING_ACTION_PER_TIME
                              * framework.frame_time) % 4
        player.death_time -= framework.frame_time
        if player.death_time < 0:
            player.add_event(RESPAWN_TIMER)


    @staticmethod
    def draw(player):
        player.dying_images[int(player.dying_frame)].draw(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)

class RespawnState:
    @staticmethod
    def enter(player, event):
        if event == RESPAWN_TIMER:
            player.respawn_time = 2.5

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.respawn_time -= framework.frame_time
        if player.respawn_time < 0:
            player.add_event(READY_TIMER)

    @staticmethod
    def draw(player):
        pass


next_state_table = {

    ReadyState: {RIGHT_UP: ReadyState, LEFT_UP: ReadyState,
                 RIGHT_DOWN: ReadyState, LEFT_DOWN: ReadyState,
                 SPACE_DOWN: ReadyState, SPACE_UP: ReadyState,
                 READY_TIMER: IdleState},

    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,
                SPACE_DOWN: IdleState, SPACE_UP: IdleState,
                DEAD_TIMER: DeadState},

    DeadState: {RIGHT_UP: DeadState, LEFT_UP: DeadState,
                RIGHT_DOWN: DeadState, LEFT_DOWN: DeadState,
                SPACE_DOWN: DeadState, SPACE_UP: DeadState,
                RESPAWN_TIMER: RespawnState},

    RespawnState: {RIGHT_UP: RespawnState, LEFT_UP: RespawnState,
                   RIGHT_DOWN: RespawnState, LEFT_DOWN: RespawnState,
                   SPACE_DOWN: RespawnState, SPACE_UP: RespawnState,
                   READY_TIMER: ReadyState}
}




class StarShip:
    def __init__(self):
        self.x, self.y = 300, 50

        self.starship_image = load_image('Image/player_17.png')
        self.dying_images = [load_image('Image/explosion0_39.png'), load_image('Image/explosion1_39.png'),
                             load_image('Image/explosion2_39.png'), load_image('Image/explosion3_39.png')]
        self.life = 3
        self.velocity = 0

        self.ready_time = 0
        self.death_time = 0
        self.respawn_time = 0

        self.dying_frame = 0

        self.event_que = []
        self.cur_state = ReadyState
        self.cur_state.enter(self, READY_TIMER)

        gameworld.add_object(self, 1)

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




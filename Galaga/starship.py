from pico2d import *

import framework
import gameworld
import state_StageMain

from bullet_player import PlayerBullet


RIGHT_DOWN, LEFT_DOWN, SPACE_DOWN, RIGHT_UP, LEFT_UP, SPACE_UP, DEAD_TIMER = range(7)

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


class IdleState:
    @staticmethod
    def enter(starship, event=None):
        if event == RIGHT_DOWN and not starship.right_down:
            starship.velocity += PLAYER_SPEED_PPS
            starship.right_down = True
        elif event == LEFT_DOWN and not starship.left_down:
            starship.velocity -= PLAYER_SPEED_PPS
            starship.left_down = True
        elif event == RIGHT_UP and starship.right_down:
            starship.velocity -= PLAYER_SPEED_PPS
            starship.right_down = False
        elif event == LEFT_UP and starship.left_down:
            starship.velocity += PLAYER_SPEED_PPS
            starship.left_down = False

    @staticmethod
    def exit(starship, event=None):
        if event == SPACE_DOWN:
            starship.shoot()

    @staticmethod
    def do(starship):
        starship.x += starship.velocity * framework.frame_time
        starship.x = clamp(25, starship.x, 600 - 25)
        # player.add_event(DEAD_TIMER)

    @staticmethod
    def draw(starship):
        starship.starship_image.draw(starship.x, starship.y, PLAYER_SIZE, PLAYER_SIZE)


class DeadState:
    @staticmethod
    def enter(starship, event=None):
        if event == DEAD_TIMER:
            starship.death_time = TIME_PER_DYING_ACTION

    @staticmethod
    def exit(starship, event=None):
        gameworld.remove_object(starship)
        del starship

    @staticmethod
    def do(starship):
        starship.dying_frame = (starship.dying_frame + FRAMES_PER_DYING_ACTION * DYING_ACTION_PER_TIME
                                * framework.frame_time) % 4
        starship.death_time -= framework.frame_time
        if starship.death_time < 0:
            starship.cur_state.exit(starship, None)


    @staticmethod
    def draw(starship):
        starship.explode_images[int(starship.dying_frame)].\
            draw(starship.x, starship.y, PLAYER_SIZE * 1.7, PLAYER_SIZE * 1.7)


next_state_table = {

    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,
                SPACE_DOWN: IdleState, SPACE_UP: IdleState,
                DEAD_TIMER: DeadState},

    DeadState: {RIGHT_UP: DeadState, LEFT_UP: DeadState,
                RIGHT_DOWN: DeadState, LEFT_DOWN: DeadState,
                SPACE_DOWN: DeadState, SPACE_UP: DeadState},

}


class StarShip:
    starship_image = None
    explode_images = None

    def __init__(self):
        self.x, self.y = 300, 100

        if StarShip.starship_image is None:
            StarShip.starship_image = load_image('Image/player_17.png')
        if StarShip.explode_images is None:
            StarShip.explode_images = [load_image('Image/explosion0_39.png'), load_image('Image/explosion1_39.png'),
                                       load_image('Image/explosion2_39.png'), load_image('Image/explosion3_39.png')]

        self.velocity = 0
        self.left_down = False
        self.right_down = False

        self.death_time = 0
        self.dying_frame = 0

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self)

        self.shoot_sound = load_wav('Sound/Bullet.wav')
        self.explode_sound = load_wav('Sound/PlayerDie.wav')
        self.explode_sound.set_volume(128)

    def get_pos(self):
        return self.x, self.y

    def set_velocity_zero(self):
        self.velocity = 0

    def shoot(self):
        self.shoot_sound.play()
        bullet = PlayerBullet(self.x, self.y + 25)
        gameworld.add_object(bullet, 1)
        state_StageMain.starship_bullets.append(bullet)

    def explode(self):
        self.explode_sound.play()
        self.add_event(DEAD_TIMER)

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 10

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

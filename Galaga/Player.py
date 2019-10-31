from pico2d import *

import gameworld

# Player의 상태를 바꾸는 외부/내부 이벤트
RIGHT_DOWN, LEFT_DOWN, SPACE_DOWN, RIGHT_UP, LEFT_UP, SPACE_UP, DEAD_TIMER, ATTACK_TIMER = range(8)

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
            player.velocity += 1
        elif event == LEFT_DOWN:
            player.velocity -= 1
        elif event == RIGHT_UP:
            player.velocity -= 1
        elif event == LEFT_UP:
            player.velocity += 1


    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.x += player.velocity
        player.x = clamp(25, player.x, 600 - 25)

    @staticmethod
    def draw(player):
        player.image.draw(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)


class AttackState:
    @staticmethod
    def enter(player, event):
        gameworld.add_object(Bullet(player.x), 1)
        # 전 상태가 IdleState 일 때만 타이머를 추가하고 싶다
        player.timer = 10

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.timer -= 1
        if player.timer == 0:
            player.add_event(ATTACK_TIMER)

        player.x += player.velocity
        player.x = clamp(25, player.x, 600 - 25)


    @staticmethod
    def draw(player):
        player.image.draw(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)

class DeadState:
    @staticmethod
    def enter(player, event):
        player.timer = 0

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
                SPACE_DOWN: AttackState, SPACE_UP: IdleState,
                DEAD_TIMER: DeadState},


    AttackState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                  RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,
                  SPACE_DOWN: IdleState, SPACE_UP: IdleState,
                  DEAD_TIMER: DeadState, ATTACK_TIMER: IdleState},


    DeadState: {RIGHT_UP: DeadState, LEFT_UP: DeadState,
                RIGHT_DOWN: DeadState, LEFT_DOWN: DeadState,
                SPACE_DOWN: DeadState, SPACE_UP: DeadState,
                DEAD_TIMER: IdleState}
}


PLAYER_POSITION_Y = 50
PLAYER_SIZE = 50
PLAYER_SPEED = 1


class Player:
    def __init__(self):
        self.x, self.y = 300, PLAYER_POSITION_Y
        self.region = []
        self.image = load_image('Image/player_17.png')
        self.dead_image = [load_image('Image/explosion0_39.png'), load_image('Image/explosion1_39.png'),
                           load_image('Image/explosion2_39.png'), load_image('Image/explosion3_39.png')]
        self.life = 3
        self.velocity = 0
        self.dead_frame = 0
        self.timer = 0

        self.event_que = []

        self.cur_state = IdleState
        self.cur_state.enter(self, None)

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



class Bullet:
    image = None

    def __init__(self, x):
        self.x, self.y = x, PLAYER_POSITION_Y + 23
        if Bullet.image == None:
            Bullet.image = load_image('Image/player_bullet_9.png')

    def update(self):
        if self.y > 800:
            gameworld.remove_object(self)
        for enemy in gameworld.all_objects():
            # if type(enemy) == 적이라면: 충돌체크
            pass
        self.y += 2

    def draw(self):
        self.image.draw(self.x, self.y, 10, 10)
import framework
from pico2d import *

PLAYER_POSITION_Y = 40
PLAYER_SIZE = 50
PLAYER_SPEED = 2

# 클래스
class Player:
    def __init__(self):
        self.x, self.y = 300, PLAYER_POSITION_Y
        self.image = load_image('Image/player_17.png')
        self.dir = 0

    def update_position(self):
        next_position = self.x + self.dir * PLAYER_SPEED
        if next_position < 50 or next_position > 550:
            return
        else:
            self.x = next_position



# 변수 선언
background_image = None
player = None

def enter():
    global background_image
    global player
    background_image = load_image('Image/background_basic.png')
    player = Player()

def exit():
    global background_image
    del background_image

def puase():
    pass

def resume():
    pass

def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                player.dir += 1
            elif event.key == SDLK_LEFT:
                player.dir -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                player.dir -= 1
            elif event.key == SDLK_LEFT:
                player.dir += 1


def update():
    player.update_position()

def draw():
    clear_canvas()
    background_image.draw(framework.CLIENT_WIDTH / 2, framework.CLIENT_HEIGHT / 2)
    player.image.draw(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)
    update_canvas()
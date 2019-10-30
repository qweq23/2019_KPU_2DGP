import framework
from pico2d import *

from Player import *


# 변수 선언
background_image = None
background_front_stars1 = None
background_front_stars2 = None
background_front_frame = 0
player = None

front_stars_pos = 0
# 별: x = 300, y = 400 ~ 1200

def enter():
    global background_image
    global background_front_stars1
    global background_front_stars2
    global player

    background_image = load_image('Image/background_basic.png')
    background_front_stars1 = load_image('Image/background_front1.png')
    background_front_stars2 = load_image('Image/background_front2.png')
    player = Player()


def exit():
    global background_image
    global background_front_stars1
    global background_front_stars2

    del background_image
    del background_front_stars1
    del background_front_stars2

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
            player.control(SDL_KEYDOWN, event.key)
        elif event.type == SDL_KEYUP:
            player.control(SDL_KEYUP, event.key)


def update():
    global front_stars_pos
    global background_front_frame
    player.update_position()
    front_stars_pos = (front_stars_pos + 1) % 800
    background_front_frame = (background_front_frame + 1) % 200



def draw():
    global background_image
    global background_front_stars1
    global background_front_stars2
    global front_stars_pos
    global background_front_frame

    clear_canvas()
    background_image.draw(framework.CLIENT_WIDTH / 2, framework.CLIENT_HEIGHT / 2)
    if background_front_frame < 100:
        background_front_stars1.clip_draw(0, front_stars_pos, 600, 800, 300, 400)
    else:
        background_front_stars2.clip_draw(0, front_stars_pos, 600, 800, 300, 400)

    player.draw()
    update_canvas()


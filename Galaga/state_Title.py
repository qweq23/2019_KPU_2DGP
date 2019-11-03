import framework
from pico2d import *

import state_Main

name = "TitleState"
background_image = None
background_front_stars1 = None
background_front_stars2 = None
background_front_frame = 0
front_stars_pos = 0
title_image = None
title_frame = 0
timer = 0
press_enter_to_start = None

def enter():
    global background_image
    global background_front_stars1
    global background_front_stars2
    global title_image
    global press_enter_to_start
    background_image = load_image('Image/title_background.png')
    background_front_stars1 = load_image('Image/background_front1.png')
    background_front_stars2 = load_image('Image/background_front2.png')
    title_image = [load_image('Image/title_Galaga0.png'), load_image('Image/title_Galaga1.png'),
                   load_image('Image/title_Galaga2.png'), load_image('Image/title_Galaga3.png'),
                   load_image('Image/title_Galaga4.png'), load_image('Image/title_Galaga3.png'),
                   load_image('Image/title_Galaga2.png'), load_image('Image/title_Galaga1.png')]
    press_enter_to_start = load_image('Image/press_enter_to_start.png')

def exit():
    global background_image
    global title_image

    del background_image
    del title_image


def pause():
    pass
def resume():
    pass


def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.running = False
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            framework.change_state(state_Main)


def update():
    global title_frame
    global front_stars_pos
    global background_front_frame

    title_frame = (title_frame + 1) % 80
    front_stars_pos = (front_stars_pos + 1) % 800
    background_front_frame = (background_front_frame + 1) % 200
    delay(0.001)

def draw():
    global background_image
    global background_front_stars1
    global background_front_stars2
    global front_stars_pos
    global title_image

    clear_canvas()
    background_image.draw(framework.CLIENT_WIDTH / 2, framework.CLIENT_HEIGHT / 2)

    if background_front_frame < 100:
        background_front_stars1.clip_draw(0, front_stars_pos, 600, 800, 400, 400)
    else:
        background_front_stars2.clip_draw(0, front_stars_pos, 600, 800, 400, 400)

    title_image[title_frame // 10].draw(framework.CLIENT_WIDTH / 2, 500)
    press_enter_to_start.draw(framework.CLIENT_WIDTH / 2, 200)
    update_canvas()

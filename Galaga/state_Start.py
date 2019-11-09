import framework
from pico2d import *

import state_Title

name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    image = load_image('Image/kpu_credit.png')


def exit():
    global image
    del image


def pause():
    pass


def resume():
    pass


def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.running = False


def update():
    global logo_time
    if logo_time > 1.5:
        logo_time = 0
        framework.change_state(state_Title)

    logo_time += framework.frame_time


def draw():
    global image
    clear_canvas()
    image.draw(framework.CLIENT_WIDTH / 2, framework.CLIENT_HEIGHT / 2)
    update_canvas()
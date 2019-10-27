import framework
from pico2d import *

import state_main

name = "TitleState"
background_image = None
title_image = None
frame = 0


def enter():
    global background_image
    global title_image
    background_image = load_image('Image/title_background.png')
    title_image = [load_image('Image/title_Galaga0.png'), load_image('Image/title_Galaga1.png'),
                   load_image('Image/title_Galaga2.png'), load_image('Image/title_Galaga3.png'),
                   load_image('Image/title_Galaga4.png'), load_image('Image/title_Galaga3.png'),
                   load_image('Image/title_Galaga2.png'), load_image('Image/title_Galaga1.png')]

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
            framework.change_state(state_main)



def update():
    global frame
    frame = (frame + 1) % 8
    delay(0.1)

def draw():
    global background_image
    global title_image

    clear_canvas()
    background_image.draw(framework.CLIENT_WIDTH / 2, framework.CLIENT_HEIGHT / 2)
    title_image[frame].draw(framework.CLIENT_WIDTH / 2, 500)
    update_canvas()

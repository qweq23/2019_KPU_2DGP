import framework
from pico2d import *

import state_main

name = "TitleState"
background_image = None



def enter():
    pass
def exit():
    pass

def pause():
    pass
def resume():
    pass


def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.running = False
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_k):
            framework.change_state(state_main)



def update():
    pass
def draw():
    pass
from pico2d import *
import framework
import gameworld

import state_Title

from background_black import BackGround
from stars import BG_Stars


name = "EndingState"
background = None
stars = None

def enter():
    gameworld.clear()

    global background
    background = BackGround()

    global stars
    stars = BG_Stars(400, get_canvas_height() / 2)


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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            framework.push_state(state_Title)


def update():
    background.update()
    stars.update()

def draw():
    clear_canvas()

    background.draw()
    stars.draw()

    framework.font.draw(250, 400, 'Press enter to Restart', (251, 100, 0))
    update_canvas()


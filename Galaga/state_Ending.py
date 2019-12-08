from pico2d import *
import framework
import gameworld

import state_Title

from background_black import BackGround
from stars import BG_Stars


name = "EndingState"


def enter():
    background = BackGround()
    stars = BG_Stars(400, get_canvas_height() / 2)


def exit():
    gameworld.clear()


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
    for gameobj in gameworld.all_objects():
        gameobj.update()


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    framework.font.draw(250, 400, 'Press enter to Restart', (251, 100, 0))
    update_canvas()


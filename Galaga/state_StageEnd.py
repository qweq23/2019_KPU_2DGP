from pico2d import *
import framework
import gameworld

import state_Pause
import state_Ranking

from starship import StarShip

END_TIMER = 4

name = "StageEndState"
ui = None
starship = None
timer = END_TIMER


def enter():
    global ui
    ui = gameworld.get_ui()

    global starship
    for gameobj in gameworld.all_objects():
        if isinstance(gameobj, StarShip):
            starship = gameobj
            break


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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            framework.push_state(state_Pause)
        else:
            if starship is not None:
                starship.handle_event(event)


def update():
    global timer
    timer -= framework.frame_time

    for gameobj in gameworld.all_objects():
        gameobj.update()

    if timer < 0:
        framework.change_state(state_Ranking)


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    update_canvas()


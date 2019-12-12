from pico2d import *
import framework
import gameworld

import state_Pause

from starship import StarShip

REGEN_TIME = 6

name = "StageRegenState"
font = None
ui = None
timer = REGEN_TIME


def enter():
    global ui
    ui = gameworld.get_ui()

    global font
    font = load_font('Font/LCD_Solid.ttf', 24)

    global timer
    timer = REGEN_TIME


def exit():
    starship = StarShip()
    gameworld.add_object(starship, 1)


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


def update():
    global timer
    timer -= framework.frame_time

    for gameobj in gameworld.all_objects():
        gameobj.update()

    if timer < 0:
        framework.pop_state()


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    if timer < 2:
        font.draw(250, 400, 'Ready', (251, 100, 0))

    update_canvas()


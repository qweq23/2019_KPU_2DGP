from pico2d import *
import framework
import gameworld

import state_Pause
import state_StageMain

from starship import StarShip

name = "StageEnterState"
ui = None
font = None
starship = None
timer = 5
stage_num = 0


def enter():
    global ui
    ui = gameworld.get_ui()

    global stage_num
    stage_num = ui.get_stage_num()

    global font
    font = load_font('Font/LCD_Solid.ttf', 24)

    global starship
    for gameobj in gameworld.all_objects():
        if isinstance(gameobj, StarShip):
            starship = gameobj
            break


def exit():
    global timer
    timer = 5


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
            starship.handle_event(event)


def update():
    global timer
    timer -= framework.frame_time

    for gameobj in gameworld.all_objects():
        gameobj.update()

    if timer < 0:
        framework.change_state(state_StageMain)


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    if timer > 3:
        font.draw(250, 400, 'Stage %d' % stage_num, (251, 100, 0))
    elif timer > 2:
        pass
    else:
        font.draw(250, 400, 'Ready', (251, 100, 0))

    update_canvas()


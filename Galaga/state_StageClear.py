from pico2d import *
import framework
import gameworld

import state_Pause
import state_StageEnter
import state_Ranking

from starship import StarShip

# event type: (EVENT, VALUE)
LIFE, STAGE, SCORE = range(3)

CLEAR_TIME = 2

name = "StageClearState"
ui = None
font = None
starship = None
timer = CLEAR_TIME


def enter():
    print('clear enter')
    global ui
    ui = gameworld.get_ui()

    global starship
    for gameobj in gameworld.all_objects():
        if isinstance(gameobj, StarShip):
            starship = gameobj
            break

    global font
    font = load_font('Font/LCD_Solid.ttf', 24)


def exit():
    global timer
    timer = CLEAR_TIME
    ui.add_event((STAGE, 1))
    ui.update()


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
        if ui.get_stage_num() == 5:
            framework.change_state(state_Ranking)
            return
        framework.change_state(state_StageEnter)


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    # font.draw(250, 400, 'perfect!', (255, 0, 0))

    update_canvas()


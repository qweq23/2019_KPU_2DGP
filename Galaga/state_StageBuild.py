from pico2d import *
import framework
import gameworld

import state_Pause

from background_black import BackGround
from stars import BG_Stars
from UI_manager import UI_Manager


name = "StageBuildState"
font = None
timer = 2


def enter():
    background = BackGround()
    gameworld.add_object(background, 0)

    stars = BG_Stars(300, get_canvas_height() / 2)
    gameworld.add_object(stars, 0)

    ui = UI_Manager()
    gameworld.add_object(ui, 1)

    global font
    font = load_font('Font/LCD_Solid.ttf', 24)


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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            framework.push_state(state_Pause)


def update():
    global timer
    timer = framework.frame_time
    if timer < 0:
        pass


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    font.draw(250, 400, 'Start', (251, 100, 0))

    update_canvas()


from pico2d import *
import framework
import gameworld

import state_Pause
import state_StageEnter

from background_black import BackGround
from stars import BG_Stars
from UI_manager import UI_Manager
from starship import StarShip

name = "StageBuildState"
font = None
timer = 2
stars = None


def enter():
    background = BackGround()
    gameworld.add_object(background, 0)

    ui = UI_Manager()
    gameworld.register_ui(ui)

    global stars
    stars = BG_Stars(300, get_canvas_height() / 2)
    gameworld.add_object(stars, 0)

    global font
    font = load_font('Font/LCD_Solid.ttf', 24)


def exit():
    stars.move()
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
        framework.change_state(state_StageEnter)


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    font.draw(250, 400, 'Start', (251, 100, 0))

    update_canvas()


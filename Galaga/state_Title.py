import framework
from pico2d import *

import state_StageBuild

from background_black import BackGround
from stars import Stars
from gamelogo import GameLogo

name = "TitleState"

background = None
stars = None
game_logo = None
font = None


def enter():
    global background
    background = BackGround()

    global stars
    stars = Stars(400, get_canvas_height() / 2)

    global game_logo
    game_logo = GameLogo()

    global font
    font = load_font('Font/LCD_Solid.ttf', 24)


def exit():
    global background
    global stars
    global game_logo

    del background
    del stars
    del game_logo


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
            framework.change_state(state_StageBuild)


def update():
    stars.update()
    game_logo.update()


def draw():
    clear_canvas()

    background.draw()
    stars.draw()
    game_logo.draw()
    font.draw(250, 200, 'Press enter to start', (251, 100, 0))

    update_canvas()

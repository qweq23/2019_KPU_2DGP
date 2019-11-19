import framework
from pico2d import *

import state_Main

import gameworld

from stars import BG_Stars
from gamelogo import GameLogo
from background_black import BackGround

name = "TitleState"


def enter():
    background = BackGround()
    stars = BG_Stars(framework.CLIENT_WIDTH / 2, framework.CLIENT_HEIGHT / 2)
    game_logo = GameLogo()


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
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            framework.change_state(state_Main)


def update():
    for gameobj in gameworld.all_objects():
        gameobj.update()


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()
    framework.font.draw(250, 200, 'Press enter to start', (251, 100, 0))

    update_canvas()

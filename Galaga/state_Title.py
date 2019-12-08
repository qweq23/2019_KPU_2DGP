import framework
from pico2d import *

import state_Main
import state_StageBuild

from gamelogo import GameLogo

name = "TitleState"

background_image = None
stars_image = []
game_logo = None
font = None

stars_frame = 0


def enter():
    global background_image
    global stars_image
    global game_logo
    global font

    background_image = load_image('Image/background_black_800.png')
    game_logo = GameLogo()
    stars_image = [load_image('Image/stars1_800.png'), load_image('Image/stars2_800.png')]
    font = load_font('Font/LCD_Solid.ttf', 24)


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
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            framework.change_state(state_StageBuild)


def update():
    global stars_frame
    stars_frame = (stars_frame + framework.frame_time * 1.5) % 2
    game_logo.update()


def draw():
    clear_canvas()

    background_image.draw(get_canvas_width() / 2, get_canvas_height() / 2)
    stars_image[int(stars_frame)].draw(get_canvas_width() / 2, get_canvas_width() / 2)
    game_logo.draw()
    font.draw(250, 200, 'Press enter to start', (251, 100, 0))

    update_canvas()

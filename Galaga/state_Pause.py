import framework
from pico2d import *

import gameworld

pause_button_image = None


def enter():
    global pause_button_image
    pause_button_image = load_image('Image/pause_button_29.png')


def exit():
    global pause_button_image
    del pause_button_image


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.quit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            framework.pop_state()


def update():
    pass


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()
    pause_button_image.draw(300, 400, 50, 50)

    update_canvas()

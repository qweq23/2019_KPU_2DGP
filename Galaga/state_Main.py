from pico2d import *
import framework
import gameworld

import state_Pause
import state_Ending

from background_black import BackGround
from stars import BG_Stars
from UI_manager import UI_Manager
from stage import Stage


name = "MainState"
stage = None
ui = None
ui_event_que = []


def enter():
    background = BackGround()
    gameworld.add_object(background, 0)

    stars = BG_Stars(300, get_canvas_height() / 2)
    gameworld.add_object(stars, 0)

    global stage
    stage = Stage()

    global ui
    ui = UI_Manager()


def exit():
    gameworld.clear()


def pause():
    # 플레이어가 속도를 가지고 있다면, 0으로 만들어줘야 한다
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
            stage.handle_event(event)


def update():
    for gameobj in gameworld.all_objects():
        gameobj.update()

    # ui event 넘겨주기
    event = stage.put_ui_event()

    if event is not None:
        ui.add_event(event)


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    update_canvas()


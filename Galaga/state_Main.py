from pico2d import *
import framework
import gameworld

import state_Pause

# state_Main에서 할 일
# 1. 게임 월드의 객체를 업데이트하고, 그린다
# 2. 백그라운드 객체를 인스턴스한다. -> 백그라운드 객체, 스테이지에서 인스턴스해도 되지 않음?
# 3. 스테이지를 인스턴스한다.
# 4. UI를 인스턴스한다.

#   스테이지는 자신의 시간을 가지고, 스테이지 시간이 끝나면 다음 스테이지로 넘어간다.
#   충돌 처리는 스테이지 안에서, 포그라운드 객체의 인스턴스도 스테이지 안에서 이루어진다.

# 인스턴스 된 객체는 반드시 게임월드에 들어가는가?
# 메인 스테이트에서 백그라운드, 스테이지, UI를 조정할 일이 있을까?
# 스테이지랑 UI는 조정할 일이 있겠지만 백그라운드는 없을 것 같다, 게임월드에만 넣어주면 될 듯

# ui 매니저 객체는 여기에 인스턴스 된다. 이벤트를 넣어줄거면 여기서 넣어줘야 한다.
# 하지만 ui에 필요한 정보는 스테이트가 모두 가지고 있다. 즉 스테이트가 ui 정보가 바뀌어야 할 때 ui 관련 함수를 불러서 사용할 수 있다.
# 이거 두개를 어떻게 연결하지....


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
    stars = BG_Stars(300, get_canvas_height() / 2)

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


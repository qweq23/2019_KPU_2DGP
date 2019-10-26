from Galaga.Global import *
import os

print (os.getcwd())
background = load_image('background.png')


def game_opening():
    pass


def rendering():
    global background
    background.draw()
    pass


def update():
    pass


def handle_events():
    global isEnd

    # 이벤트들이 담긴 리스트가 넘어옴
    events = get_events();
    for  event in events:
        if event.type == SDL_QUIT:
            isEnd = True
    pass



pico2d.open_canvas(CONST_CLIENT_WIDTH, CONST_CLIENT_HEIGHT)

game_opening()
isEnd = False

# 게임 루프
while not isEnd:
    rendering()
    update()
    handle_events()

pico2d.close_canvas()

from Global import *

def game_opening():
    pass


def rendering():
    pass


def update():
    pass

def handle_events():
    pass


pico2d.open_canvas()

game_opening()
isEnd = False

# 게임 루프
while not isEnd:
    rendering()
    update()

pico2d.close_canvas()

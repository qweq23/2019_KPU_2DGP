import pico2d


def game_opening():
    pass


def rendering():
    pass


def update():
    pass


pico2d.open_canvas()

game_opening()
isEnd = False

while not isEnd:
    rendering()
    update()

pico2d.close_canvas()

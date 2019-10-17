import pico2d

client_w, client_h = 800, 600

#Game Object
class Player:
    def __init__(self):
        self.x = ClientWidth / 2
        self.life = 3


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

while not isEnd:
    rendering()
    update()

pico2d.close_canvas()

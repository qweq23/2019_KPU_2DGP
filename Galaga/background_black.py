from pico2d import *

class BackGround:
    def __init__(self):
        self.image = load_image('Image/background_black_800.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(get_canvas_width() / 2, get_canvas_height() / 2)
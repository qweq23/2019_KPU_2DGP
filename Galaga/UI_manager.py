from pico2d import *
import gameworld

class UI_Manager:
    def __init__(self):
        self.life = 3
        self.stage = 1
        self.score = 0

        self.life_image = load_image('Image/player_17.png')
        self.stage_image = load_image('Image/stages_ui_sprite_95x19.png')
        self.font = load_font('Font/LCD_Solid.ttf', 24)  # DRAW SCORE

        gameworld.add_object(self, 0)

    def update(self):
        pass

    def draw(self):
        pass

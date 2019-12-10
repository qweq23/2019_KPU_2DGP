from pico2d import *

# event type: (EVENT, VALUE)
LIFE, STAGE, SCORE = range(3)


class UI_Manager:
    def __init__(self):
        self.event_que = []

        self.ui_data = {
            LIFE: 3,
            STAGE: 1,
            SCORE: 0,
        }

        # self.frame = 0 필요할까?
        self.frame_image = load_image('Image/ui_frame_200x800.png')
        self.life_image = load_image('Image/player_17.png')
        self.stage_image = load_image('Image/stages_ui_sprite_95x19.png')
        self.font = load_font('Font/LCD_Solid.ttf', 24)  # DRAW SCORE

    def get_starship_life(self):
        return self.ui_data[LIFE]

    def get_stage_num(self):
        return self.ui_data[STAGE]

    def get_score(self):
        return self.ui_data[SCORE]

    def add_event(self, event):
        self.event_que.append(event)

    def update(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.ui_data[event[0]] += event[1]

    def draw(self):
        self.frame_image.draw(700, 400)

        self.font.draw(600 + 20, 760, 'SCORE', (255, 0, 0))
        self.font.draw(600 + 20, 720, '%d' % self.ui_data[SCORE], (255, 255, 255))

        for i in range(0, self.ui_data[LIFE]):
            self.life_image.draw(620 + 25 + (i * 55), 600, 50, 50)

        self.stage_image.clip_draw((5 - self.ui_data[STAGE]) * 19, 0, 19, 19, 620 + 25, 400, 50, 50)


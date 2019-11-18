from pico2d import *
import gameworld


# event type: (EVENT, VALUE)
LIFE, STAGE, SCORE = range(3)


class UI_Manager:
    def __init__(self):
        self.event_que = []

        self.life = 3
        self.stage_number = 1
        self.score = 0

        self.event_table = {
            LIFE: self.life,
            STAGE: self.stage_number,
            SCORE: self.score
        }

        # self.frame = 0 필요할까?
        self.frame_image = load_image('Image/ui_frame_200x800.png')
        self.life_image = load_image('Image/player_17.png')
        self.stage_image = load_image('Image/stages_ui_sprite_95x19.png')
        self.font = load_font('Font/LCD_Solid.ttf', 24)  # DRAW SCORE

        gameworld.add_object(self, 0)

    def add_event(self, event):
        self.event_que.append(event)

    def update(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if event[0] == LIFE:
                pass
            elif event[0] == STAGE:
                self.stage_number += event[1]
            elif event == SCORE:
                pass

    def draw(self):
        self.frame_image.draw(700, 400)

        self.font.draw(600 + 20, 760, 'SCORE', (255, 0, 0))
        self.font.draw(600 + 20, 720, '%d' % self.score, (255, 255, 255))

        for i in range(0, self.life):
            self.life_image.draw(620 + 25 + (i * 55), 600, 50, 50)

        self.stage_image.clip_draw((5 - self.stage_number) * 19, 0, 19, 19, 620 + 25, 400, 50, 50)


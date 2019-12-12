from pico2d import *
import json
import datetime

import framework
import gameworld

import state_Title

from background_black import BackGround
from stars import Stars


name = "EndingState"
sound = None
background = None
stars = None
new_records = []
score = 0
current_rank = 0


def save_score():
    global new_records
    with open('record_data.json', 'r') as f:
        data_str = f.read()
        if len(data_str) == 0:
            data_str = '[]'
        data = json.loads(data_str)
        new_records = data

        new_records.append(score)
        new_records.sort()
        new_records.reverse()

        if len(new_records) > 10:
            new_records.pop()

    with open('record_data.json', 'w') as f:
        data_str = json.dumps(new_records)
        f.write(data_str)


def get_current_rank():
    global current_rank
    reversed_records = new_records
    reversed_records.reverse()

    for rank in range(len(reversed_records)):
        if reversed_records[rank] == score:
            current_rank = len(reversed_records) - rank
            print(current_rank)
            break

    reversed_records.reverse()


def enter():
    global sound
    sound = load_music('Sound/Credits.wav')
    sound.repeat_play()

    global new_records
    new_records = []

    global score
    ui = gameworld.get_ui()
    score = ui.get_score()
    save_score()
    get_current_rank()

    gameworld.clear()

    global background
    background = BackGround()

    global stars
    stars = Stars(400, get_canvas_height() / 2)




def exit():
    global sound
    del sound

    global background
    del background

    global stars
    del stars


def pause():
    pass


def resume():
    pass


def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            framework.push_state(state_Title)
            sound.stop()


def update():
    background.update()
    stars.update()


def draw():
    clear_canvas()

    background.draw()
    stars.draw()

    framework.font.draw(360, 750, 'SCORE', (255, 0, 0))
    framework.font.draw(360, 710, '%05d' % score, (255, 255, 255))
    framework.font.draw(360, 600, 'TOP10', (255, 0, 0))

    for i in range(len(new_records)):
        if i + 1 == current_rank:
            framework.font.draw(200, 500 - (i * 40), '%2d.      %5d' % (i + 1, new_records[i]), (255, 255, 0))
        else:
            framework.font.draw(200, 500 - (i * 40), '%2d.      %5d' % (i + 1, new_records[i]), (0, 255, 255))

    update_canvas()


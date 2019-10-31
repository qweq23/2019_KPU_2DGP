import framework
from pico2d import *

import gameworld

from player import Player
from enemy import Bee

# 변수 선언
background_image = None
background_front_stars1 = None
background_front_stars2 = None
background_front_frame = 0
player = None



# test
test_enemy = []

front_stars_pos = 0
# 별: x = 300, y = 400 ~ 1200

def enter():
    global background_image
    global background_front_stars1
    global background_front_stars2
    global player

    global test_enemy

    background_image = load_image('Image/background_basic.png')
    background_front_stars1 = load_image('Image/background_front1.png')
    background_front_stars2 = load_image('Image/background_front2.png')
    player = Player()
    test_enemy = [Bee(100, 600), Bee(200, 600), Bee(300, 600),
                  Bee(400, 600), Bee(500, 600)]
    gameworld.add_object(player, 1)
    gameworld.add_objects(test_enemy, 1)


def exit():
    global background_image
    global background_front_stars1
    global background_front_stars2

    del background_image
    del background_front_stars1
    del background_front_stars2

    gameworld.clear()

def puase():
    pass

def resume():
    pass

def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.running = False
        else:
            player.handle_event(event)


def update():
    global front_stars_pos
    global background_front_frame

    front_stars_pos = (front_stars_pos + 1) % 800
    background_front_frame = (background_front_frame + 1) % 200

    for gameobj in gameworld.all_objects():
        gameobj.update()



def draw():
    global background_image
    global background_front_stars1
    global background_front_stars2
    global front_stars_pos
    global background_front_frame

    clear_canvas()
    background_image.draw(framework.CLIENT_WIDTH / 2, framework.CLIENT_HEIGHT / 2)
    if background_front_frame < 100:
        background_front_stars1.clip_draw(0, front_stars_pos, 600, 800, 300, 400)
    else:
        background_front_stars2.clip_draw(0, front_stars_pos, 600, 800, 300, 400)

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    update_canvas()


import framework
from pico2d import *

from gameobject import *


# 변수 선언
background_image = None
player = None
bullet = None


def enter():
    global background_image
    global player
    global bullet
    background_image = load_image('Image/background_basic.png')
    player = Player()
    bullet = Bullet(300)

def exit():
    global background_image
    del background_image

def puase():
    pass

def resume():
    pass

def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.running = False
        elif event.type == SDL_KEYDOWN:
            player.control(SDL_KEYDOWN, event.key)
        elif event.type == SDL_KEYUP:
            player.control(SDL_KEYUP, event.key)


def update():
    player.update_position()
    bullet.update_position()
    bullet.detect_collision()

def draw():
    clear_canvas()
    background_image.draw(framework.CLIENT_WIDTH / 2, framework.CLIENT_HEIGHT / 2)
    player.draw()
    bullet.draw()
    update_canvas()
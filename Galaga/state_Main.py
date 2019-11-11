import framework
from pico2d import *

import gameworld

from background_black import BackGround
from stars import BG_Stars

from starship import StarShip
from enemy import Bee
from enemy import Butterfly
from enemy import Moth
from bullet_player import PlayerBullet

name = "MainState"

# 변수 선언

player = None


enemies = []
player_bullets = []
enemy_bullets = []

front_stars_pos = 0
# 별: x = 300, y = 400 ~ 1200


def enter():
    global player
    global enemies

    background = BackGround()
    stars = BG_Stars(300, framework.CLIENT_HEIGHT / 2)
    player = StarShip()
    enemies = [Bee(100, 600), Bee(200, 600), Bee(300, 600),
               Bee(400, 600), Bee(500, 600)]

    gameworld.add_objects([background, stars], 0)
    gameworld.add_object(player, 1)
    gameworld.add_objects(enemies, 1)


def exit():
    gameworld.clear()


def pause():
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
    global player_bullets, enemy_bullets

    front_stars_pos = (front_stars_pos + 1) % 800

    for gameobj in gameworld.all_objects():
        gameobj.update()
        if isinstance(gameobj, PlayerBullet):
            player_bullets.append(gameobj)

    # 플레이어:적, 플레이어: 총알, 적:총알
    for enemy in enemies:
        if collide(player, enemy):
            print("COLLISION")
            # 적은 사라지고 나는 터짐

        for bullet in player_bullets:
            if collide(bullet, enemy):
                print("COLLISION")
                gameworld.remove_object(bullet)
                enemy.die()
                enemies.remove(enemy)
                player_bullets.remove(bullet)
                break


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    update_canvas()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

from pico2d import *
import framework
import gameworld

import state_Pause
import state_StageRegen
import state_StageClear
import state_StageEnd

from starship import StarShip
from enemyline import Line

name = "StageMainState"

# event type: (EVENT, VALUE)
LIFE, STAGE, SCORE = range(3)
ui = None

starship = None
line = None
enemies = []
starship_bullets = []
enemy_bullets = []


def hit_starship():
    starship.explode()
    ui.add_event((LIFE, -1))
    ui.update()
    if ui.get_starship_life() == 0:
        framework.change_state(state_StageEnd)
    else:
        framework.push_state(state_StageRegen)



def intersect_bb(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def enter():
    global ui
    ui = gameworld.get_ui()

    global starship
    for gameobj in gameworld.all_objects():
        if isinstance(gameobj, StarShip):
            starship = gameobj
            break

    global line
    line = Line()
    line.generate_enemy(ui.get_stage_num())

    global enemies
    enemies = line.get_enemies_list()


def exit():
    pass


def pause():
    pass


def resume():
    global starship
    for gameobj in gameworld.all_objects():
        if isinstance(gameobj, StarShip):
            starship = gameobj
            break

    starship.set_velocity_zero()


def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            framework.push_state(state_Pause)
        else:
            starship.handle_event(event)


def update():
    for gameobj in gameworld.all_objects():
        gameobj.update()

    for bullet in starship_bullets:
        for enemy in enemies:
            if intersect_bb(bullet, enemy):
                enemy.hit()
                starship_bullets.remove(bullet)
                gameworld.remove_object(bullet)
                break

    for bullet in enemy_bullets:
        if intersect_bb(starship, bullet):
            enemy_bullets.remove(bullet)
            gameworld.remove_object(bullet)
            hit_starship()
            break

    for enemy in enemies:
        if intersect_bb(starship, enemy):
            enemy.hit()
            hit_starship()
            break

    # 총알이 클라이언트 밖에 나갔나 검사
    for bullet in starship_bullets:
        if bullet.out_client():
            starship_bullets.remove(bullet)
            gameworld.remove_object(bullet)
            break

    for bullet in enemy_bullets:
        if bullet.out_client():
            enemy_bullets.remove(bullet)
            gameworld.remove_object(bullet)
            break

    if len(enemies) == 0:
        framework.change_state(state_StageClear)


def draw():
    clear_canvas()

    for gameobj in gameworld.all_objects():
        gameobj.draw()

    update_canvas()

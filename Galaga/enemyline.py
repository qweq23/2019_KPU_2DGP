from pico2d import *

import gameworld

from bee import Bee
from butterfly import Butterfly
from moth import Moth

# 하나의 파트 당 8마리의 적들을 인스턴스한다.
# 프로그램 하기 편하려면, 파트별 리스트도 필요하고, 실제 위치별 리스트도 필요하다.

BEE, BFLY, MOTH = range(3)
coord_x = [75, 125, 175, 225, 275, 325, 375, 425, 475, 525]
coord_y = [700, 650, 600, 550, 500]

# {stage_num: {part: [enemy list]}}
enemy_generation_table = {
    1: {0: [BFLY, BFLY, BFLY, BFLY, BEE, BEE, BEE, BEE],
        1: [MOTH, MOTH, MOTH, MOTH, BFLY, BFLY, BFLY, BFLY],
        2: [BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY],
        3: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        4: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        },
    2: {0: [BFLY, BFLY, BFLY, BFLY, BEE, BEE, BEE, BEE],
        1: [MOTH, MOTH, MOTH, MOTH, BFLY, BFLY, BFLY, BFLY],
        2: [BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY],
        3: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        4: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        },
    3: {0: [BFLY, BFLY, BFLY, BFLY, BEE, BEE, BEE, BEE],
        1: [MOTH, MOTH, MOTH, MOTH, BFLY, BFLY, BFLY, BFLY],
        2: [BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY],
        3: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        4: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        },
    4: {0: [BFLY, BFLY, BFLY, BFLY, BEE, BEE, BEE, BEE],
        1: [MOTH, MOTH, MOTH, MOTH, BFLY, BFLY, BFLY, BFLY],
        2: [BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY],
        3: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        4: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        },
    5: {0: [BFLY, BFLY, BFLY, BFLY, BEE, BEE, BEE, BEE],
        1: [MOTH, MOTH, MOTH, MOTH, BFLY, BFLY, BFLY, BFLY],
        2: [BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY, BFLY],
        3: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        4: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        },
}

# {part : [(x, y)]}
enemy_position_table = {
    0: [(coord_x[4], coord_y[1]), (coord_x[5], coord_y[1]), (coord_x[4], coord_y[2]), (coord_x[5], coord_y[2]),
        (coord_x[4], coord_y[3]), (coord_x[5], coord_y[3]), (coord_x[4], coord_y[4]), (coord_x[5], coord_y[4])],

    1: [(coord_x[3], coord_y[0]), (coord_x[4], coord_y[0]), (coord_x[5], coord_y[0]), (coord_x[6], coord_y[0]),
        (coord_x[3], coord_y[1]), (coord_x[6], coord_y[1]), (coord_x[3], coord_y[2]), (coord_x[6], coord_y[2])],

    2: [(coord_x[1], coord_y[1]), (coord_x[2], coord_y[1]), (coord_x[7], coord_y[1]), (coord_x[8], coord_y[1]),
        (coord_x[1], coord_y[2]), (coord_x[2], coord_y[2]), (coord_x[7], coord_y[2]), (coord_x[8], coord_y[2])],

    3: [(coord_x[2], coord_y[3]), (coord_x[3], coord_y[3]), (coord_x[6], coord_y[3]), (coord_x[7], coord_y[3]),
        (coord_x[2], coord_y[4]), (coord_x[3], coord_y[4]), (coord_x[6], coord_y[4]), (coord_x[7], coord_y[4])],

    4: [(coord_x[0], coord_y[3]), (coord_x[1], coord_y[3]), (coord_x[8], coord_y[3]), (coord_x[9], coord_y[3]),
        (coord_x[0], coord_y[4]), (coord_x[1], coord_y[4]), (coord_x[8], coord_y[4]), (coord_x[9], coord_y[4])],
}


class Line:
    def __init__(self):
        # [part0, part1, part2, part3, part4]
        self.enemies = [[], [], [], [], []]

    def generate_enemy(self, stage_num):
        enemy_dic = enemy_generation_table[stage_num]

        for part_num in range(len(self.enemies)):
            enemy_part = enemy_dic[part_num]

            number = 0
            for enemy_type in enemy_part:
                enemy = None
                if enemy_type == BEE:
                    enemy = Bee(enemy_position_table[part_num][number])
                elif enemy_type == BFLY:
                    enemy = Butterfly(enemy_position_table[part_num][number])
                elif enemy_type == MOTH:
                    enemy = Moth(enemy_position_table[part_num][number])

                self.enemies[part_num].append(enemy)
                number += 1

            gameworld.add_objects(self.enemies[part_num], 1)

    def get_enemies_list(self):
        enemies = []
        for i in range(len(self.enemies)):
            enemies += self.enemies[i]
        return enemies





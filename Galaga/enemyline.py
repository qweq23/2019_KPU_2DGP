from pico2d import *
import random as r

import framework
import gameworld

import state_StageMain

from bee import Bee
from butterfly import Butterfly
from moth import Moth
from BehaviorTree import BehaviorTree, LeafNode, SelectorNode, SequenceNode


BEE, BFLY, MOTH = range(3)
coord_x = [75, 125, 175, 225, 275, 325, 375, 425, 475, 525]
coord_y = [700, 650, 600, 550, 500]

# {stage_num: {part: [enemy list]}}
enemy_generation_table = {
    1: {0: [BFLY, BFLY, BFLY, BFLY, BEE, BEE, BEE, BEE],
        1: [MOTH, MOTH, MOTH, MOTH, BFLY, BFLY, BFLY, BFLY],
        2: [],
        3: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        4: [],
        },
    2: {0: [BFLY, BFLY, BFLY, BFLY, BEE, BEE, BEE, BEE],
        1: [MOTH, MOTH, MOTH, MOTH, BFLY, BFLY, BFLY, BFLY],
        2: [],
        3: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        4: [BEE, BEE, BEE, BEE, BEE, BEE, BEE, BEE],
        },
    3: {0: [BFLY, BFLY, BFLY, BFLY, BEE, BEE, BEE, BEE],
        1: [MOTH, MOTH, MOTH, MOTH, BFLY, BFLY, BFLY, BFLY],
        2: [],
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

attack_timer_table = {
    0: 3,
    1: 3,
    2: 2,
    3: 2,
    4: 1,
}


class Line:
    def __init__(self):
        # [part0, part1, part2, part3, part4]
        self.enemies = [[], [], [], [], []]

        self.stage_num = 0
        self.attack_timer = 0

        self.bt = None
        self.build_behavior_tree()

    def update(self):
        self.attack_timer -= framework.frame_time
        if self.attack_timer < 0:
            self.attack_timer = attack_timer_table[self.stage_num]
            self.order_attack()

    def order_attack(self):
        number_of_enemy = len(state_StageMain.enemies)
        num1 = r.randint(0, number_of_enemy - 1)
        num2 = r.randint(0, number_of_enemy - 1)

        if not state_StageMain.enemies[num1].is_attack_state():
            state_StageMain.enemies[num1].attack(state_StageMain.get_starship_pos())
        if not state_StageMain.enemies[num2].is_attack_state():
            state_StageMain.enemies[num2].attack(state_StageMain.get_starship_pos())
            print('order attack')

    def generate_enemy(self, stage_num):
        print(stage_num)
        self.stage_num = stage_num - 1
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
                else:
                    pass

                self.enemies[part_num].append(enemy)
                number += 1

            gameworld.add_objects(self.enemies[part_num], 1)

    def get_enemies_list(self):
        enemies = []
        for i in range(len(self.enemies)):
            enemies += self.enemies[i]
        return enemies

    def build_behavior_tree(self):
        root_node = SequenceNode('Root')
        part1_enter_node = SequenceNode('Part1 Enter')
        part2_enter_node = SequenceNode('Part2 Enter')
        part3_enter_node = SequenceNode('Part3 Enter')
        part4_enter_node = SequenceNode('Part4 Enter')
        part5_enter_node = SequenceNode('Part5 Enter')
        attack_node = SequenceNode('Attack')

        root_node.add_children(part1_enter_node, part2_enter_node, part3_enter_node,
                               part4_enter_node, part5_enter_node, attack_node)
        self.bt = BehaviorTree(root_node)


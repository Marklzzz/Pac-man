import os
import pygame
from typing import List, Optional, Set

from maps import nodes_matrix, Cell


def find_path(start_node: Cell, end_node: Cell) -> Optional[List[Cell]]:
    global nodes_matrix

    start_node.cost = 0

    reachable = [start_node]
    explored = []

    while reachable:
        node = choose_node(reachable, end_node)

        if not node:
            return None
        if node == end_node:
            return build_path(end_node)

        del reachable[reachable.index(node)]
        explored.append(node)

        new_reachable = get_adjacent_nodes(node) - set(explored)
        for adjacent in new_reachable:
            if adjacent not in reachable:
                reachable.append(adjacent)

            if node.cost + 1 < adjacent.cost:
                adjacent.previous = node
                adjacent.cost = node.cost + 1

    for line in nodes_matrix:
        for cell in line:
            cell.reset()

    return None


def get_adjacent_nodes(node: Cell) -> Set[Cell]:
    x, y = node.x, node.y
    adjacent = set()
    global nodes_matrix
    for s_x in (-1, 0, 1):
        for s_y in (-1, 0, 1):
            if (
                0 not in (s_x, s_y) or
                (s_x, s_y) == (0, 0) or
                len(nodes_matrix) == y + s_y or
                len(nodes_matrix[0]) == x + s_x or
                -1 in (y + s_y, x + s_x)
            ):
                continue
            cur_node = nodes_matrix[y + s_y][x + s_x]
            if cur_node.type == 'field':
                adjacent.add(cur_node)
    return adjacent


def build_path(to_node: Cell) -> List[Cell]:
    global nodes_matrix
    path = []
    while to_node != None:
        path.append(to_node)
        to_node = to_node.previous

    for line in nodes_matrix:
        for cell in line:
            cell.reset()

    return path


def choose_node(reachable: List[Cell], goal_node: Cell) -> Cell:
    min_cost = 100
    best_node = None

    for node in reachable:
        cost_start_to_node = node.cost
        cost_node_to_goal = abs(node.x - goal_node.x) + abs(node.y - goal_node.y)
        total_cost = cost_start_to_node + cost_node_to_goal

        if min_cost > total_cost:
            min_cost = total_cost
            best_node = node

    return best_node


def create_full_matrix(matrix):
    for i in range(len(matrix)):
        matrix[i] = [*matrix[i], *matrix[i][::-1]]
    return matrix


matrix_part = [

]

matrix_full = create_full_matrix(matrix_part)

for i in matrix_full:
    print(i)
pygame.init()

size = 960, 960
screen = pygame.display.set_mode(size)
size_of_parts = 28

class Field:
    global screen, size_of_parts

    def __init__(self):
        self.wall_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты ↑.png'),
                                             (size_of_parts, size_of_parts))
        self.wall_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты ←.png'),
                                             (size_of_parts, size_of_parts))
        self.wall_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты →.png'),
                                             (size_of_parts, size_of_parts))
        self.wall_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты ↓.png'),
                                             (size_of_parts, size_of_parts))

        self.spicific_angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑→.png'),
                                                       (size_of_parts, size_of_parts))
        self.spicific_angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑←.png'),
                                                       (size_of_parts, size_of_parts))
        self.spicific_angle_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ←↓.png'),
                                                       (size_of_parts, size_of_parts))
        self.spicific_angle_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ←↓.png'),
                                                       (size_of_parts, size_of_parts))


        self.angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↑←.png'),
                                              (size_of_parts, size_of_parts))
        self.angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↑→.png'),
                                              (size_of_parts, size_of_parts))
        self.angle_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↓←.png'),
                                              (size_of_parts, size_of_parts))
        self.angle_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↓←.png'),
                                              (size_of_parts, size_of_parts))
        self.angle_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↓→.png'),
                                              (size_of_parts, size_of_parts))

        self.frame_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока →.png'),
                                              (size_of_parts, size_of_parts))
        self.frame_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока ←.png'),
                                              (size_of_parts, size_of_parts))
        self.frame_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока ↑.png'),
                                              (size_of_parts, size_of_parts))
        self.frame_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока ↓.png'),
                                              (size_of_parts, size_of_parts))

        self.angle_frame_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока ↑←.png'),
                                                    (size_of_parts, size_of_parts))
        self.angle_frame_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока ↑→.png'),
                                                    (size_of_parts, size_of_parts))
        self.angle_frame_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока ↓←.png'),
                                                    (size_of_parts, size_of_parts))
        self.angle_frame_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока ↓→.png'),
                                                    (size_of_parts, size_of_parts))

        self.Z = pygame.transform.scale(pygame.image.load('data/mazeparts/Z-переход.png'),
                                                    (size_of_parts, size_of_parts))
        self.S = pygame.transform.scale(pygame.image.load('data/mazeparts/S-переход.png'),
                                        (size_of_parts, size_of_parts))
        self.M = pygame.transform.scale(pygame.image.load('data/mazeparts/M-переход.png'),
                                        (size_of_parts, size_of_parts))
        self.W = pygame.transform.scale(pygame.image.load('data/mazeparts/W-переход.png'),
                                        (size_of_parts, size_of_parts))

        self.rotate_angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/центр поворот ↑→.png'),
                                        (size_of_parts, size_of_parts))

        self.rotate_angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/центр поворот ↑←.png'),
                                                     (size_of_parts, size_of_parts))
        self.make_first_line()
        self.make_second_line()
        self.make_third_line()
        self.make_fourth_line()
        self.make_fifth_line()
        self.make_sixth_line()
        self.make_seventh_line()
        self.make_eight_line()
        self.make_nine_line()
        self.make_tenth_line()
        self.make_eleventh_line()
        self.make_twelfth_line()
        self.make_thirteenth_line()
        self.make_fourteenth_line()
        self.make_fifteenth_line()
        self.make_sixteenth_line()
        self.make_seventeenth_line()
        self.make_eighteenth_line()
        self.make_nineteenth_line()

    def make_first_line(self):
        screen.blit(self.angle_1, (0, 0))
        for i in range(1, 13):
            screen.blit(self.wall_1, (i * size_of_parts, 0))
        screen.blit(self.spicific_angle_1, (size_of_parts * 13, 0))
        screen.blit(self.spicific_angle_2, (size_of_parts * 14, 0))
        for i in range(1, 13):
            screen.blit(self.wall_1, (size_of_parts * 14 + i * size_of_parts, 0))
        screen.blit(self.angle_2, (size_of_parts * 27, 0))

    def make_second_line(self):
        screen.blit(self.wall_2, (0, size_of_parts))
        screen.blit(self.frame_1, (size_of_parts * 13, size_of_parts))
        screen.blit(self.frame_2, (size_of_parts * 14, size_of_parts))
        screen.blit(self.wall_3, (size_of_parts * 27, size_of_parts))

    def make_third_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 2))

        screen.blit(self.angle_frame_1, (size_of_parts * 2, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 3, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 4, size_of_parts * 2))
        screen.blit(self.angle_frame_2, (size_of_parts * 5, size_of_parts * 2))

        screen.blit(self.angle_frame_1, (size_of_parts * 7, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 8, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 9, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 10, size_of_parts * 2))
        screen.blit(self.angle_frame_2, (size_of_parts * 11, size_of_parts * 2))

        screen.blit(self.frame_1, (size_of_parts * 13, size_of_parts * 2))
        screen.blit(self.frame_2, (size_of_parts * 14, size_of_parts * 2))

        screen.blit(self.angle_frame_1, (size_of_parts * 16, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 17, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 18, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 19, size_of_parts * 2))
        screen.blit(self.angle_frame_2, (size_of_parts * 20, size_of_parts * 2))

        screen.blit(self.angle_frame_1, (size_of_parts * 22, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 23, size_of_parts * 2))
        screen.blit(self.frame_4, (size_of_parts * 24, size_of_parts * 2))
        screen.blit(self.angle_frame_2, (size_of_parts * 25, size_of_parts * 2))

        screen.blit(self.wall_3, (size_of_parts * 27, size_of_parts * 2))

    def make_fourth_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 3))

        screen.blit(self.frame_1, (size_of_parts * 2, size_of_parts * 3))
        screen.blit(self.frame_2, (size_of_parts * 5, size_of_parts * 3))

        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 3))
        screen.blit(self.frame_2, (size_of_parts * 11, size_of_parts * 3))

        screen.blit(self.frame_1, (size_of_parts * 13, size_of_parts * 3))
        screen.blit(self.frame_2, (size_of_parts * 14, size_of_parts * 3))

        screen.blit(self.frame_2, (size_of_parts * 16, size_of_parts * 3))
        screen.blit(self.frame_1, (size_of_parts * 20, size_of_parts * 3))

        screen.blit(self.frame_1, (size_of_parts * 22, size_of_parts * 3))
        screen.blit(self.frame_2, (size_of_parts * 25, size_of_parts * 3))

        screen.blit(self.wall_3, (size_of_parts * 27, size_of_parts * 3))

    def make_fifth_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 4))

        screen.blit(self.angle_frame_3, (size_of_parts * 2, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 3, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 4, size_of_parts * 4))
        screen.blit(self.angle_frame_4, (size_of_parts * 5, size_of_parts * 4))

        screen.blit(self.angle_frame_3, (size_of_parts * 7, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 8, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 9, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 10, size_of_parts * 4))
        screen.blit(self.angle_frame_4, (size_of_parts * 11, size_of_parts * 4))

        screen.blit(self.angle_frame_3, (size_of_parts * 13, size_of_parts * 4))
        screen.blit(self.angle_frame_4, (size_of_parts * 14, size_of_parts * 4))

        screen.blit(self.angle_frame_3, (size_of_parts * 16, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 17, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 18, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 19, size_of_parts * 4))
        screen.blit(self.angle_frame_4, (size_of_parts * 20, size_of_parts * 4))

        screen.blit(self.angle_frame_3, (size_of_parts * 22, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 23, size_of_parts * 4))
        screen.blit(self.frame_4, (size_of_parts * 24, size_of_parts * 4))
        screen.blit(self.angle_frame_4, (size_of_parts * 25, size_of_parts * 4))

        screen.blit(self.wall_3, (size_of_parts * 27, size_of_parts * 4))

    def make_sixth_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 5))
        screen.blit(self.wall_3, (size_of_parts * 27, size_of_parts * 5))

    def make_seventh_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 6))

        screen.blit(self.angle_frame_1, (size_of_parts * 2, size_of_parts * 6))
        screen.blit(self.frame_3, (size_of_parts * 3, size_of_parts * 6))
        screen.blit(self.frame_3, (size_of_parts * 4, size_of_parts * 6))
        screen.blit(self.angle_frame_2, (size_of_parts * 5, size_of_parts * 6))

        screen.blit(self.angle_frame_1, (size_of_parts * 7, size_of_parts * 6))
        screen.blit(self.angle_frame_2, (size_of_parts * 8, size_of_parts * 6))

        screen.blit(self.angle_frame_1, (size_of_parts * 10, size_of_parts * 6))
        for i in range(1, 7):
            screen.blit(self.frame_3, (size_of_parts * (10 + i), size_of_parts * 6))
        screen.blit(self.angle_frame_2, (size_of_parts * 17, size_of_parts * 6))

        screen.blit(self.angle_frame_1, (size_of_parts * 19, size_of_parts * 6))
        screen.blit(self.angle_frame_2, (size_of_parts * 20, size_of_parts * 6))

        screen.blit(self.angle_frame_1, (size_of_parts * 22, size_of_parts * 6))
        screen.blit(self.frame_3, (size_of_parts * 23, size_of_parts * 6))
        screen.blit(self.frame_3, (size_of_parts * 24, size_of_parts * 6))
        screen.blit(self.angle_frame_2, (size_of_parts * 25, size_of_parts * 6))

        screen.blit(self.wall_3, (size_of_parts * 27, size_of_parts * 6))

    def make_eight_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 7))

        screen.blit(self.angle_frame_3, (size_of_parts * 2, size_of_parts * 7))
        screen.blit(self.frame_4, (size_of_parts * 3, size_of_parts * 7))
        screen.blit(self.frame_4, (size_of_parts * 4, size_of_parts * 7))
        screen.blit(self.angle_frame_4, (size_of_parts * 5, size_of_parts * 7))

        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 7))
        screen.blit(self.frame_2, (size_of_parts * 8, size_of_parts * 7))

        screen.blit(self.angle_frame_3, (size_of_parts * 10, size_of_parts * 7))
        screen.blit(self.frame_4, (size_of_parts * 11, size_of_parts * 7))
        screen.blit(self.frame_4, (size_of_parts * 12, size_of_parts * 7))
        screen.blit(self.angle_frame_2, (size_of_parts * 13, size_of_parts * 7))
        screen.blit(self.angle_frame_1, (size_of_parts * 14, size_of_parts * 7))
        screen.blit(self.frame_4, (size_of_parts * 15, size_of_parts * 7))
        screen.blit(self.frame_4, (size_of_parts * 16, size_of_parts * 7))
        screen.blit(self.angle_frame_4, (size_of_parts * 17, size_of_parts * 7))

        screen.blit(self.frame_1, (size_of_parts * 19, size_of_parts * 7))
        screen.blit(self.frame_2, (size_of_parts * 20, size_of_parts * 7))

        screen.blit(self.angle_frame_3, (size_of_parts * 22, size_of_parts * 7))
        screen.blit(self.frame_4, (size_of_parts * 23, size_of_parts * 7))
        screen.blit(self.frame_4, (size_of_parts * 24, size_of_parts * 7))
        screen.blit(self.angle_frame_4, (size_of_parts * 25, size_of_parts * 7))

        screen.blit(self.wall_3, (size_of_parts * 27, size_of_parts * 7))

    def make_nine_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 8))

        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 8))
        screen.blit(self.frame_2, (size_of_parts * 8, size_of_parts * 8))

        screen.blit(self.frame_1, (size_of_parts * 13, size_of_parts * 8))
        screen.blit(self.frame_2, (size_of_parts * 14, size_of_parts * 8))

        screen.blit(self.frame_1, (size_of_parts * 19, size_of_parts * 8))
        screen.blit(self.frame_2, (size_of_parts * 20, size_of_parts * 8))

        screen.blit(self.wall_3, (size_of_parts * 27, size_of_parts * 8))

    def make_tenth_line(self):
        screen.blit(self.angle_3, (0, size_of_parts * 9))

        for i in range(1, 5):
            screen.blit(self.wall_4, (size_of_parts * i, size_of_parts * 9))
        screen.blit(self.angle_frame_2, (size_of_parts * 5, size_of_parts * 9))

        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 9))
        screen.blit(self.angle_frame_3, (size_of_parts * 8, size_of_parts * 9))

        screen.blit(self.frame_3, (size_of_parts * 9, size_of_parts * 9))
        screen.blit(self.frame_3, (size_of_parts * 10, size_of_parts * 9))
        screen.blit(self.angle_frame_2, (size_of_parts * 11, size_of_parts * 9))

        screen.blit(self.frame_1, (size_of_parts * 13, size_of_parts * 9))
        screen.blit(self.frame_2, (size_of_parts * 14, size_of_parts * 9))

        screen.blit(self.angle_frame_1, (size_of_parts * 16, size_of_parts * 9))
        screen.blit(self.frame_3, (size_of_parts * 17, size_of_parts * 9))
        screen.blit(self.frame_3, (size_of_parts * 18, size_of_parts * 9))

        screen.blit(self.angle_frame_4, (size_of_parts * 19, size_of_parts * 9))
        screen.blit(self.frame_2, (size_of_parts * 20, size_of_parts * 9))

        screen.blit(self.angle_frame_1, (size_of_parts * 22, size_of_parts * 9))
        for i in range(1, 5):
            screen.blit(self.wall_4, (size_of_parts * (22 + i), size_of_parts * 9))

        screen.blit(self.angle_4, (size_of_parts * 27, size_of_parts * 9))

    def make_eleventh_line(self):
        screen.blit(self.wall_2, (size_of_parts * 5, size_of_parts * 10))

        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 10))
        screen.blit(self.angle_frame_1, (size_of_parts * 8, size_of_parts * 10))

        screen.blit(self.frame_4, (size_of_parts * 9, size_of_parts * 10))
        screen.blit(self.frame_4, (size_of_parts * 10, size_of_parts * 10))
        screen.blit(self.angle_frame_4, (size_of_parts * 11, size_of_parts * 10))

        screen.blit(self.angle_frame_3, (size_of_parts * 13, size_of_parts * 10))
        screen.blit(self.angle_frame_4, (size_of_parts * 14, size_of_parts * 10))

        screen.blit(self.angle_frame_3, (size_of_parts * 16, size_of_parts * 10))
        screen.blit(self.frame_4, (size_of_parts * 17, size_of_parts * 10))
        screen.blit(self.frame_4, (size_of_parts * 18, size_of_parts * 10))

        screen.blit(self.angle_frame_2, (size_of_parts * 19, size_of_parts * 10))
        screen.blit(self.frame_2, (size_of_parts * 20, size_of_parts * 10))

        screen.blit(self.wall_3, (size_of_parts * 22, size_of_parts * 10))

    def make_twelfth_line(self):
        screen.blit(self.wall_2, (size_of_parts * 5, size_of_parts * 11))

        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 11))
        screen.blit(self.frame_2, (size_of_parts * 8, size_of_parts * 11))

        screen.blit(self.frame_1, (size_of_parts * 19, size_of_parts * 11))
        screen.blit(self.frame_2, (size_of_parts * 20, size_of_parts * 11))

        screen.blit(self.wall_3, (size_of_parts * 22, size_of_parts * 11))

    def make_thirteenth_line(self):
        screen.blit(self.wall_2, (size_of_parts * 5, size_of_parts * 12))

        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 12))
        screen.blit(self.frame_2, (size_of_parts * 8, size_of_parts * 12))

        screen.blit(self.frame_1, (size_of_parts * 19, size_of_parts * 12))
        screen.blit(self.frame_2, (size_of_parts * 20, size_of_parts * 12))

        screen.blit(self.wall_3, (size_of_parts * 22, size_of_parts * 12))

    def make_fourteenth_line(self):
        for i in range(0, 5):
            screen.blit(self.wall_1, (size_of_parts * i, size_of_parts * 13))
        screen.blit(self.angle_frame_4, (size_of_parts * 5, size_of_parts * 13))

        screen.blit(self.angle_frame_3, (size_of_parts * 7, size_of_parts * 13))
        screen.blit(self.angle_frame_4, (size_of_parts * 8, size_of_parts * 13))

        screen.blit(self.angle_frame_3, (size_of_parts * 19, size_of_parts * 13))
        screen.blit(self.angle_frame_4, (size_of_parts * 20, size_of_parts * 13))

        screen.blit(self.angle_frame_3, (size_of_parts * 22, size_of_parts * 13))
        for i in range(1, 6):
            screen.blit(self.wall_1, (size_of_parts * (22 + i), size_of_parts * 13))

    def make_fifteenth_line(self):
        pass

    def make_sixteenth_line(self):
        for i in range(0, 5):
            screen.blit(self.wall_4, (size_of_parts * i, size_of_parts * 15))
        screen.blit(self.angle_frame_2, (size_of_parts * 5, size_of_parts * 15))

        screen.blit(self.angle_frame_1, (size_of_parts * 7, size_of_parts * 15))
        screen.blit(self.angle_frame_2, (size_of_parts * 8, size_of_parts * 15))

        screen.blit(self.angle_frame_1, (size_of_parts * 19, size_of_parts * 15))
        screen.blit(self.angle_frame_2, (size_of_parts * 20, size_of_parts * 15))

        screen.blit(self.angle_frame_1, (size_of_parts * 22, size_of_parts * 15))
        for i in range(1, 6):
            screen.blit(self.wall_4, (size_of_parts * (22 + i), size_of_parts * 15))

    def make_seventeenth_line(self):
        screen.blit(self.wall_2, (size_of_parts * 5, size_of_parts * 16))

        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 16))
        screen.blit(self.frame_2, (size_of_parts * 8, size_of_parts * 16))

        screen.blit(self.frame_1, (size_of_parts * 19, size_of_parts * 16))
        screen.blit(self.frame_2, (size_of_parts * 20, size_of_parts * 16))

        screen.blit(self.wall_3, (size_of_parts * 22, size_of_parts * 16))

    def make_eighteenth_line(self):
        screen.blit(self.wall_2, (size_of_parts * 5, size_of_parts * 17))

        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 17))
        screen.blit(self.frame_2, (size_of_parts * 8, size_of_parts * 17))

        screen.blit(self.angle_frame_1, (size_of_parts * 10, size_of_parts * 17))
        for i in range(1, 7):
            screen.blit(self.frame_3, (size_of_parts * (10 + i), size_of_parts * 17))
        screen.blit(self.angle_frame_2, (size_of_parts * 17, size_of_parts * 17))

        screen.blit(self.frame_1, (size_of_parts * 19, size_of_parts * 17))
        screen.blit(self.frame_2, (size_of_parts * 20, size_of_parts * 17))

        screen.blit(self.wall_3, (size_of_parts * 22, size_of_parts * 17))

    def make_nineteenth_line(self):
        screen.blit(self.angle_1, (0, size_of_parts * 18))

        for i in range(1, 5):
            screen.blit(self.wall_1, (size_of_parts * i, size_of_parts * 18))
        screen.blit(self.angle_frame_4, (size_of_parts * 5, size_of_parts * 18))

        screen.blit(self.angle_frame_3, (size_of_parts * 7, size_of_parts * 18))
        screen.blit(self.angle_frame_4, (size_of_parts * 8, size_of_parts * 18))

        screen.blit(self.angle_frame_3, (size_of_parts * 10, size_of_parts * 18))
        screen.blit(self.frame_4, (size_of_parts * 11, size_of_parts * 18))
        screen.blit(self.frame_4, (size_of_parts * 12, size_of_parts * 18))
        screen.blit(self.angle_frame_2, (size_of_parts * 13, size_of_parts * 18))
        screen.blit(self.angle_frame_1, (size_of_parts * 14, size_of_parts * 18))
        screen.blit(self.frame_4, (size_of_parts * 15, size_of_parts * 18))
        screen.blit(self.frame_4, (size_of_parts * 16, size_of_parts * 18))
        screen.blit(self.angle_frame_4, (size_of_parts * 17, size_of_parts * 18))

        screen.blit(self.angle_frame_3, (size_of_parts * 19, size_of_parts * 18))
        screen.blit(self.angle_frame_4, (size_of_parts * 20, size_of_parts * 18))

        screen.blit(self.angle_frame_3, (size_of_parts * 22, size_of_parts * 18))
        for i in range(1, 5):
            screen.blit(self.wall_1, (size_of_parts * (22 + i), size_of_parts * 18))

        screen.blit(self.angle_2, (size_of_parts * 27, size_of_parts * 18))


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Pac_man:
    def __init__(self, x, y, direction):
        self.x, self.y = x, y

        self.animation = [load_image('data/pacman/left1.png', -1), load_image('data/pacman/left1.png', -1)]
        self.rect = self.animation[0].get_rect()
        self.mask = pygame.mask.from_surface(self.animation[0])
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = 180
        self.direction = direction
        self.frame = 0

    def move(self):
        if self.wall_check():
            self.x += (self.speed * self.direction[0]) / fps
            self.y += (self.speed * self.direction[1]) / fps
            self.rect.x = self.x
            self.rect.y = self.y

    def wall_check(self):
        return True


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.x, self.y = x, y

    def update(self):
        if pygame.sprite.collide_mask(self, pacman):
            self.kill()


class Point(Object, pygame.sprite.Sprite):
    image = load_image('data/other/s_food.png', -1)

    def __init__(self, x, y):
        super().__init__(x, y, points_sprite)
        self.image = Point.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Energizer(Object, pygame.sprite.Sprite):
    image = load_image('data/other/b_food.png', -1)

    def __init__(self, x, y):
        super().__init__(x, y, points_sprite)
        self.image = Energizer.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Fruits(Object):
    def __init__(self, x, y):
        super().__init__(x, y)


if __name__ == '__main__':
    fps = 60
    running = True
    point = load_image('data/other/s_food.png', -1)
    points_sprite = pygame.sprite.Group()

    pacman = Pac_man(250, 250, (0, 0))

    clock = pygame.time.Clock()
    frame = 0
    while running:
        screen.fill((0, 0, 0))
        ex = Field()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.direction = (-1, 0)
                    pacman.animation = [load_image('data/pacman/left1.png', -1),
                                        load_image('data/pacman/left2.png', -1)]
                elif event.key == pygame.K_RIGHT:
                    pacman.direction = (1, 0)
                    pacman.animation = [load_image('data/pacman/right1.png', -1),
                                        load_image('data/pacman/right2.png', -1)]
                elif event.key == pygame.K_UP:
                    pacman.direction = (0, -1)
                    pacman.animation = [load_image('data/pacman/up1.png', -1),
                                        load_image('data/pacman/up2.png', -1)]
                elif event.key == pygame.K_DOWN:
                    pacman.direction = (0, 1)
                    pacman.animation = [load_image('data/pacman/down1.png', -1),
                                        load_image('data/pacman/down2.png', -1)]

        if pacman.frame % 15 == 0:
            frame += 1
        points_sprite.draw(screen)
        screen.blit(pacman.animation[frame % 2], (pacman.x, pacman.y))
        pacman.frame += 1
        pacman.move()

        clock.tick(fps)
        pygame.display.flip()
pygame.quit()

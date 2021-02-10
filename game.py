import os
import random

import pygame, pygame.display, pygame.sprite
import pygame.font, pygame.mixer, pygame.draw
import pygame.transform, pygame.event

from typing import List, Optional, Set, Tuple
from time import sleep

from maps import nodes_matrix, Cell


def find_path(start_node: Cell, end_node: Cell) -> Optional[List[Tuple[int, int]]]:
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

        try:
            new_reachable = get_adjacent_nodes(node) - set(explored)
        except IndexError:
            return None
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


def build_path(to_node: Cell) -> List[Tuple[int, int]]:
    path = []
    while to_node != None:
        path.append(to_node)
        to_node = to_node.previous

    for line in nodes_matrix:
        for cell in line:
            cell.reset()

    sides = []
    last_n = path[-1]
    for n in list(reversed(path))[1:]:
        sides.append((n.x - last_n.x, n.y - last_n.y))
        last_n = n

    return sides


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


pygame.init()
cell_size = 24

size = 28 * cell_size, 36 * cell_size

maze = pygame.Surface(size)
screen = pygame.display.set_mode(size)

important_points = ((6, 1), (21, 1), (1, 5), (6, 5), (9, 5), (12, 5), (15, 5), (18, 5), (21, 5), (26, 5),
                    (6, 8), (21, 8), (12, 11), (15, 11), (6, 14), (9, 14), (18, 14), (21, 14), (9, 17),
                    (18, 17), (6, 20), (9, 20), (18, 20), (21, 20), (6, 23), (9, 23), (12, 23), (15, 23),
                    (18, 23), (21, 23), (3, 26), (24, 26), (12, 26), (15, 26), (26, 1))

fruits_order = [
    (), ('cherry',), ('cherry', 'strawberry'), ('cherry', 'strawberry', 'peach'),
    ('cherry', 'strawberry', 'peach', 'peach'), ('cherry', 'strawberry', 'peach', 'peach', 'apple'),
    ('cherry', 'strawberry', 'peach', 'peach', 'apple', 'apple'),
    ('cherry', 'strawberry', 'peach', 'peach', 'apple', 'apple', 'melon'),
    ('strawberry', 'peach', 'peach', 'apple', 'apple', 'melon', 'melon'),
    ('peach', 'peach', 'apple', 'apple', 'melon', 'melon', 'spaceship'),
    ('peach', 'apple', 'apple', 'melon', 'melon', 'spaceship', 'spaceship'),
    ('apple', 'apple', 'melon', 'melon', 'spaceship', 'spaceship', 'bell'),
    ('apple', 'melon', 'melon', 'spaceship', 'spaceship', 'bell', 'bell'),
    ('melon', 'melon', 'spaceship', 'spaceship', 'bell', 'bell', 'key'),
    ('melon', 'spaceship', 'spaceship', 'bell', 'bell', 'key', 'key'),
    ('spaceship', 'spaceship', 'bell', 'bell', 'key', 'key', 'key'),
    ('spaceship', 'bell', 'bell', 'key', 'key', 'key', 'key'),
    ('bell', 'bell', 'key', 'key', 'key', 'key', 'key'),
    ('bell', 'key', 'key', 'key', 'key', 'key', 'key'),
    ('key', 'key', 'key', 'key', 'key', 'key', 'key'),
]

class Field:

    def __init__(self):
        self.wall_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты ↑.png'),
                                             (cell_size, cell_size))
        self.wall_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты ←.png'),
                                             (cell_size, cell_size))
        self.wall_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты →.png'),
                                             (cell_size, cell_size))
        self.wall_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты ↓.png'),
                                             (cell_size, cell_size))

        self.spicific_angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑→.png'),
                                                       (cell_size, cell_size))
        self.spicific_angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑←.png'),
                                                       (cell_size, cell_size))
        self.spicific_angle_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ←↓.png'),
                                                       (cell_size, cell_size))
        self.spicific_angle_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты →↓.png'),
                                                       (cell_size, cell_size))
        self.spicific_angle_5 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ←↑.png'),
                                                       (cell_size, cell_size))
        self.spicific_angle_6 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты →↑.png'),
                                                       (cell_size, cell_size))

        self.angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↑←.png'),
                                              (cell_size, cell_size))
        self.angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↑→.png'),
                                              (cell_size, cell_size))
        self.angle_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↓←.png'),
                                              (cell_size, cell_size))
        self.angle_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↓←.png'),
                                              (cell_size, cell_size))
        self.angle_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↓→.png'),
                                              (cell_size, cell_size))

        self.frame_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока →.png'),
                                              (cell_size, cell_size))
        self.frame_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока ←.png'),
                                              (cell_size, cell_size))
        self.frame_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока ↑.png'),
                                              (cell_size, cell_size))
        self.frame_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока ↓.png'),
                                              (cell_size, cell_size))

        self.angle_frame_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока ↑←.png'),
                                                    (cell_size, cell_size))
        self.angle_frame_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока ↑→.png'),
                                                    (cell_size, cell_size))
        self.angle_frame_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока ↓←.png'),
                                                    (cell_size, cell_size))
        self.angle_frame_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока ↓→.png'),
                                                    (cell_size, cell_size))

        self.make_1_line()
        self.make_2_line()
        self.make_3_line()
        self.make_4_line()
        self.make_5_line()
        self.make_6_line()
        self.make_7_line()
        self.make_8_line()
        self.make_9_line()
        self.make_10_line()
        self.make_11_line()
        self.make_12_line()
        self.make_13_line()
        self.make_14_line()
        self.make_15_line()
        self.make_16_line()
        self.make_17_line()
        self.make_18_line()
        self.make_19_line()
        self.make_20_line()
        self.make_21_line()
        self.make_22_line()
        self.make_23_line()
        self.make_24_line()
        self.make_25_line()
        self.make_26_line()
        self.make_27_line()
        self.make_28_line()
        self.make_29_line()
        self.make_30_line()
        self.make_31_line()

    def update(self):
        screen.blit(maze, (0, 0))

    def make_1_line(self):
        maze.blit(self.angle_1, (0, cell_size * 3))
        for i in range(1, 13):
            maze.blit(self.wall_1, (i * cell_size, cell_size * 3))
        maze.blit(self.spicific_angle_1, (cell_size * 13, cell_size * 3))
        maze.blit(self.spicific_angle_2, (cell_size * 14, cell_size * 3))
        for i in range(1, 13):
            maze.blit(self.wall_1, (cell_size * 14 + i * cell_size, cell_size * 3))
        maze.blit(self.angle_2, (cell_size * 27, cell_size * 3))

    def make_2_line(self):
        maze.blit(self.wall_2, (0, cell_size * 4))
        maze.blit(self.frame_1, (cell_size * 13, cell_size * 4))
        maze.blit(self.frame_2, (cell_size * 14, cell_size * 4))
        maze.blit(self.wall_3, (cell_size * 27, cell_size * 4))

    def make_3_line(self):
        maze.blit(self.wall_2, (0, cell_size * 5))

        maze.blit(self.angle_frame_1, (cell_size * 2, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 3, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 4, cell_size * 5))
        maze.blit(self.angle_frame_2, (cell_size * 5, cell_size * 5))

        maze.blit(self.angle_frame_1, (cell_size * 7, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 8, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 9, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 10, cell_size * 5))
        maze.blit(self.angle_frame_2, (cell_size * 11, cell_size * 5))

        maze.blit(self.frame_1, (cell_size * 13, cell_size * 5))
        maze.blit(self.frame_2, (cell_size * 14, cell_size * 5))

        maze.blit(self.angle_frame_1, (cell_size * 16, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 17, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 18, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 19, cell_size * 5))
        maze.blit(self.angle_frame_2, (cell_size * 20, cell_size * 5))

        maze.blit(self.angle_frame_1, (cell_size * 22, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 23, cell_size * 5))
        maze.blit(self.frame_4, (cell_size * 24, cell_size * 5))
        maze.blit(self.angle_frame_2, (cell_size * 25, cell_size * 5))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 5))

    def make_4_line(self):
        maze.blit(self.wall_2, (0, cell_size * 6))

        maze.blit(self.frame_1, (cell_size * 2, cell_size * 6))
        maze.blit(self.frame_2, (cell_size * 5, cell_size * 6))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 6))
        maze.blit(self.frame_2, (cell_size * 11, cell_size * 6))

        maze.blit(self.frame_1, (cell_size * 13, cell_size * 6))
        maze.blit(self.frame_2, (cell_size * 14, cell_size * 6))

        maze.blit(self.frame_2, (cell_size * 16, cell_size * 6))
        maze.blit(self.frame_1, (cell_size * 20, cell_size * 6))

        maze.blit(self.frame_1, (cell_size * 22, cell_size * 6))
        maze.blit(self.frame_2, (cell_size * 25, cell_size * 6))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 6))

    def make_5_line(self):
        maze.blit(self.wall_2, (0, cell_size * 7))

        maze.blit(self.angle_frame_3, (cell_size * 2, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 3, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 4, cell_size * 7))
        maze.blit(self.angle_frame_4, (cell_size * 5, cell_size * 7))

        maze.blit(self.angle_frame_3, (cell_size * 7, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 8, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 9, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 10, cell_size * 7))
        maze.blit(self.angle_frame_4, (cell_size * 11, cell_size * 7))

        maze.blit(self.angle_frame_3, (cell_size * 13, cell_size * 7))
        maze.blit(self.angle_frame_4, (cell_size * 14, cell_size * 7))

        maze.blit(self.angle_frame_3, (cell_size * 16, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 17, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 18, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 19, cell_size * 7))
        maze.blit(self.angle_frame_4, (cell_size * 20, cell_size * 7))

        maze.blit(self.angle_frame_3, (cell_size * 22, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 23, cell_size * 7))
        maze.blit(self.frame_4, (cell_size * 24, cell_size * 7))
        maze.blit(self.angle_frame_4, (cell_size * 25, cell_size * 7))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 7))

    def make_6_line(self):
        maze.blit(self.wall_2, (0, cell_size * 8))
        maze.blit(self.wall_3, (cell_size * 27, cell_size * 8))

    def make_7_line(self):
        maze.blit(self.wall_2, (0, cell_size * 9))

        maze.blit(self.angle_frame_1, (cell_size * 2, cell_size * 9))
        maze.blit(self.frame_3, (cell_size * 3, cell_size * 9))
        maze.blit(self.frame_3, (cell_size * 4, cell_size * 9))
        maze.blit(self.angle_frame_2, (cell_size * 5, cell_size * 9))

        maze.blit(self.angle_frame_1, (cell_size * 7, cell_size * 9))
        maze.blit(self.angle_frame_2, (cell_size * 8, cell_size * 9))

        maze.blit(self.angle_frame_1, (cell_size * 10, cell_size * 9))
        for i in range(1, 7):
            maze.blit(self.frame_3, (cell_size * (10 + i), cell_size * 9))
        maze.blit(self.angle_frame_2, (cell_size * 17, cell_size * 9))

        maze.blit(self.angle_frame_1, (cell_size * 19, cell_size * 9))
        maze.blit(self.angle_frame_2, (cell_size * 20, cell_size * 9))

        maze.blit(self.angle_frame_1, (cell_size * 22, cell_size * 9))
        maze.blit(self.frame_3, (cell_size * 23, cell_size * 9))
        maze.blit(self.frame_3, (cell_size * 24, cell_size * 9))
        maze.blit(self.angle_frame_2, (cell_size * 25, cell_size * 9))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 9))

    def make_8_line(self):
        maze.blit(self.wall_2, (0, cell_size * 10))

        maze.blit(self.angle_frame_3, (cell_size * 2, cell_size * 10))
        maze.blit(self.frame_4, (cell_size * 3, cell_size * 10))
        maze.blit(self.frame_4, (cell_size * 4, cell_size * 10))
        maze.blit(self.angle_frame_4, (cell_size * 5, cell_size * 10))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 10))
        maze.blit(self.frame_2, (cell_size * 8, cell_size * 10))

        maze.blit(self.angle_frame_3, (cell_size * 10, cell_size * 10))
        maze.blit(self.frame_4, (cell_size * 11, cell_size * 10))
        maze.blit(self.frame_4, (cell_size * 12, cell_size * 10))
        maze.blit(self.angle_frame_2, (cell_size * 13, cell_size * 10))
        maze.blit(self.angle_frame_1, (cell_size * 14, cell_size * 10))
        maze.blit(self.frame_4, (cell_size * 15, cell_size * 10))
        maze.blit(self.frame_4, (cell_size * 16, cell_size * 10))
        maze.blit(self.angle_frame_4, (cell_size * 17, cell_size * 10))

        maze.blit(self.frame_1, (cell_size * 19, cell_size * 10))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 10))

        maze.blit(self.angle_frame_3, (cell_size * 22, cell_size * 10))
        maze.blit(self.frame_4, (cell_size * 23, cell_size * 10))
        maze.blit(self.frame_4, (cell_size * 24, cell_size * 10))
        maze.blit(self.angle_frame_4, (cell_size * 25, cell_size * 10))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 10))

    def make_9_line(self):
        maze.blit(self.wall_2, (0, cell_size * 11))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 11))
        maze.blit(self.frame_2, (cell_size * 8, cell_size * 11))

        maze.blit(self.frame_1, (cell_size * 13, cell_size * 11))
        maze.blit(self.frame_2, (cell_size * 14, cell_size * 11))

        maze.blit(self.frame_1, (cell_size * 19, cell_size * 11))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 11))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 11))

    def make_10_line(self):
        maze.blit(self.angle_3, (0, cell_size * 12))

        for i in range(1, 5):
            maze.blit(self.wall_4, (cell_size * i, cell_size * 12))
        maze.blit(self.angle_frame_2, (cell_size * 5, cell_size * 12))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 12))
        maze.blit(self.angle_frame_3, (cell_size * 8, cell_size * 12))

        maze.blit(self.frame_3, (cell_size * 9, cell_size * 12))
        maze.blit(self.frame_3, (cell_size * 10, cell_size * 12))
        maze.blit(self.angle_frame_2, (cell_size * 11, cell_size * 12))

        maze.blit(self.frame_1, (cell_size * 13, cell_size * 12))
        maze.blit(self.frame_2, (cell_size * 14, cell_size * 12))

        maze.blit(self.angle_frame_1, (cell_size * 16, cell_size * 12))
        maze.blit(self.frame_3, (cell_size * 17, cell_size * 12))
        maze.blit(self.frame_3, (cell_size * 18, cell_size * 12))

        maze.blit(self.angle_frame_4, (cell_size * 19, cell_size * 12))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 12))

        maze.blit(self.angle_frame_1, (cell_size * 22, cell_size * 12))
        for i in range(1, 5):
            maze.blit(self.wall_4, (cell_size * (22 + i), cell_size * 12))

        maze.blit(self.angle_4, (cell_size * 27, cell_size * 12))

    def make_11_line(self):
        maze.blit(self.wall_2, (cell_size * 5, cell_size * 13))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 13))
        maze.blit(self.angle_frame_1, (cell_size * 8, cell_size * 13))

        maze.blit(self.frame_4, (cell_size * 9, cell_size * 13))
        maze.blit(self.frame_4, (cell_size * 10, cell_size * 13))
        maze.blit(self.angle_frame_4, (cell_size * 11, cell_size * 13))

        maze.blit(self.angle_frame_3, (cell_size * 13, cell_size * 13))
        maze.blit(self.angle_frame_4, (cell_size * 14, cell_size * 13))

        maze.blit(self.angle_frame_3, (cell_size * 16, cell_size * 13))
        maze.blit(self.frame_4, (cell_size * 17, cell_size * 13))
        maze.blit(self.frame_4, (cell_size * 18, cell_size * 13))

        maze.blit(self.angle_frame_2, (cell_size * 19, cell_size * 13))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 13))

        maze.blit(self.wall_3, (cell_size * 22, cell_size * 13))

    def make_12_line(self):
        maze.blit(self.wall_2, (cell_size * 5, cell_size * 14))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 14))
        maze.blit(self.frame_2, (cell_size * 8, cell_size * 14))

        maze.blit(self.frame_1, (cell_size * 19, cell_size * 14))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 14))

        maze.blit(self.wall_3, (cell_size * 22, cell_size * 14))

    def make_13_line(self):
        maze.blit(self.wall_2, (cell_size * 5, cell_size * 15))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 15))
        maze.blit(self.frame_2, (cell_size * 8, cell_size * 15))

        maze.blit(self.angle_frame_1, (cell_size * 10, cell_size * 15))
        maze.blit(self.wall_4, (cell_size * 11, cell_size * 15))
        maze.blit(self.wall_4, (cell_size * 12, cell_size * 15))

        maze.blit(self.wall_4, (cell_size * 15, cell_size * 15))
        maze.blit(self.wall_4, (cell_size * 16, cell_size * 15))
        maze.blit(self.angle_frame_2, (cell_size * 17, cell_size * 15))

        maze.blit(self.frame_1, (cell_size * 19, cell_size * 15))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 15))

        maze.blit(self.wall_3, (cell_size * 22, cell_size * 15))

    def make_14_line(self):
        for i in range(0, 5):
            maze.blit(self.wall_1, (cell_size * i, cell_size * 16))
        maze.blit(self.angle_frame_4, (cell_size * 5, cell_size * 16))

        maze.blit(self.angle_frame_3, (cell_size * 7, cell_size * 16))
        maze.blit(self.angle_frame_4, (cell_size * 8, cell_size * 16))

        maze.blit(self.wall_3, (cell_size * 10, cell_size * 16))
        maze.blit(self.wall_2, (cell_size * 17, cell_size * 16))

        maze.blit(self.angle_frame_3, (cell_size * 19, cell_size * 16))
        maze.blit(self.angle_frame_4, (cell_size * 20, cell_size * 16))

        maze.blit(self.angle_frame_3, (cell_size * 22, cell_size * 16))
        for i in range(1, 6):
            maze.blit(self.wall_1, (cell_size * (22 + i), cell_size * 16))

    def make_15_line(self):
        maze.blit(self.wall_3, (cell_size * 10, cell_size * 17))
        maze.blit(self.wall_2, (cell_size * 17, cell_size * 17))

    def make_16_line(self):
        for i in range(0, 5):
            maze.blit(self.wall_4, (cell_size * i, cell_size * 18))
        maze.blit(self.angle_frame_2, (cell_size * 5, cell_size * 18))

        maze.blit(self.angle_frame_1, (cell_size * 7, cell_size * 18))
        maze.blit(self.angle_frame_2, (cell_size * 8, cell_size * 18))

        maze.blit(self.wall_3, (cell_size * 10, cell_size * 18))
        maze.blit(self.wall_2, (cell_size * 17, cell_size * 18))

        maze.blit(self.angle_frame_1, (cell_size * 19, cell_size * 18))
        maze.blit(self.angle_frame_2, (cell_size * 20, cell_size * 18))

        maze.blit(self.angle_frame_1, (cell_size * 22, cell_size * 18))
        for i in range(1, 6):
            maze.blit(self.wall_4, (cell_size * (22 + i), cell_size * 18))

    def make_17_line(self):
        maze.blit(self.wall_2, (cell_size * 5, cell_size * 19))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 19))
        maze.blit(self.frame_2, (cell_size * 8, cell_size * 19))

        maze.blit(self.angle_frame_3, (cell_size * 10, cell_size * 19))
        maze.blit(self.wall_1, (cell_size * 11, cell_size * 19))
        maze.blit(self.wall_1, (cell_size * 12, cell_size * 19))
        maze.blit(self.wall_1, (cell_size * 13, cell_size * 19))
        maze.blit(self.wall_1, (cell_size * 14, cell_size * 19))
        maze.blit(self.wall_1, (cell_size * 15, cell_size * 19))
        maze.blit(self.wall_1, (cell_size * 16, cell_size * 19))
        maze.blit(self.angle_frame_4, (cell_size * 17, cell_size * 19))

        maze.blit(self.frame_1, (cell_size * 19, cell_size * 19))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 19))

        maze.blit(self.wall_3, (cell_size * 22, cell_size * 19))

    def make_18_line(self):
        maze.blit(self.wall_2, (cell_size * 5, cell_size * 20))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 20))
        maze.blit(self.frame_2, (cell_size * 8, cell_size * 20))

        maze.blit(self.frame_1, (cell_size * 19, cell_size * 20))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 20))

        maze.blit(self.wall_3, (cell_size * 22, cell_size * 20))

    def make_19_line(self):
        maze.blit(self.wall_2, (cell_size * 5, cell_size * 21))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 21))
        maze.blit(self.frame_2, (cell_size * 8, cell_size * 21))

        maze.blit(self.angle_frame_1, (cell_size * 10, cell_size * 21))
        for i in range(1, 7):
            maze.blit(self.frame_3, (cell_size * (10 + i), cell_size * 21))
        maze.blit(self.angle_frame_2, (cell_size * 17, cell_size * 21))

        maze.blit(self.frame_1, (cell_size * 19, cell_size * 21))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 21))

        maze.blit(self.wall_3, (cell_size * 22, cell_size * 21))

    def make_20_line(self):
        maze.blit(self.angle_1, (0, cell_size * 22))

        for i in range(1, 5):
            maze.blit(self.wall_1, (cell_size * i, cell_size * 22))
        maze.blit(self.angle_frame_4, (cell_size * 5, cell_size * 22))

        maze.blit(self.angle_frame_3, (cell_size * 7, cell_size * 22))
        maze.blit(self.angle_frame_4, (cell_size * 8, cell_size * 22))

        maze.blit(self.angle_frame_3, (cell_size * 10, cell_size * 22))
        maze.blit(self.frame_4, (cell_size * 11, cell_size * 22))
        maze.blit(self.frame_4, (cell_size * 12, cell_size * 22))
        maze.blit(self.angle_frame_2, (cell_size * 13, cell_size * 22))
        maze.blit(self.angle_frame_1, (cell_size * 14, cell_size * 22))
        maze.blit(self.frame_4, (cell_size * 15, cell_size * 22))
        maze.blit(self.frame_4, (cell_size * 16, cell_size * 22))
        maze.blit(self.angle_frame_4, (cell_size * 17, cell_size * 22))

        maze.blit(self.angle_frame_3, (cell_size * 19, cell_size * 22))
        maze.blit(self.angle_frame_4, (cell_size * 20, cell_size * 22))

        maze.blit(self.angle_frame_3, (cell_size * 22, cell_size * 22))
        for i in range(1, 5):
            maze.blit(self.wall_1, (cell_size * (22 + i), cell_size * 22))

        maze.blit(self.angle_2, (cell_size * 27, cell_size * 22))

    def make_21_line(self):
        maze.blit(self.wall_2, (0, cell_size * 23))

        maze.blit(self.frame_2, (cell_size * 13, cell_size * 23))
        maze.blit(self.frame_1, (cell_size * 14, cell_size * 23))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 23))

    def make_22_line(self):
        maze.blit(self.wall_2, (0, cell_size * 24))

        maze.blit(self.angle_frame_1, (cell_size * 2, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 3, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 4, cell_size * 24))
        maze.blit(self.angle_frame_2, (cell_size * 5, cell_size * 24))

        maze.blit(self.angle_frame_1, (cell_size * 7, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 8, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 9, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 10, cell_size * 24))
        maze.blit(self.angle_frame_2, (cell_size * 11, cell_size * 24))

        maze.blit(self.frame_2, (cell_size * 13, cell_size * 24))
        maze.blit(self.frame_1, (cell_size * 14, cell_size * 24))

        maze.blit(self.angle_frame_1, (cell_size * 16, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 17, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 18, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 19, cell_size * 24))
        maze.blit(self.angle_frame_2, (cell_size * 20, cell_size * 24))

        maze.blit(self.angle_frame_1, (cell_size * 22, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 23, cell_size * 24))
        maze.blit(self.frame_4, (cell_size * 24, cell_size * 24))
        maze.blit(self.angle_frame_2, (cell_size * 25, cell_size * 24))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 24))

    def make_23_line(self):
        maze.blit(self.wall_2, (0, cell_size * 25))

        maze.blit(self.angle_frame_3, (cell_size * 2, cell_size * 25))
        maze.blit(self.frame_3, (cell_size * 3, cell_size * 25))
        maze.blit(self.angle_frame_2, (cell_size * 4, cell_size * 25))
        maze.blit(self.frame_2, (cell_size * 5, cell_size * 25))

        maze.blit(self.angle_frame_3, (cell_size * 7, cell_size * 25))
        maze.blit(self.frame_3, (cell_size * 8, cell_size * 25))
        maze.blit(self.frame_3, (cell_size * 9, cell_size * 25))
        maze.blit(self.frame_3, (cell_size * 10, cell_size * 25))
        maze.blit(self.angle_frame_4, (cell_size * 11, cell_size * 25))

        maze.blit(self.angle_frame_3, (cell_size * 13, cell_size * 25))
        maze.blit(self.angle_frame_4, (cell_size * 14, cell_size * 25))

        maze.blit(self.angle_frame_3, (cell_size * 16, cell_size * 25))
        maze.blit(self.frame_3, (cell_size * 17, cell_size * 25))
        maze.blit(self.frame_3, (cell_size * 18, cell_size * 25))
        maze.blit(self.frame_3, (cell_size * 19, cell_size * 25))
        maze.blit(self.angle_frame_4, (cell_size * 20, cell_size * 25))

        maze.blit(self.frame_1, (cell_size * 22, cell_size * 25))
        maze.blit(self.angle_frame_1, (cell_size * 23, cell_size * 25))
        maze.blit(self.frame_3, (cell_size * 24, cell_size * 25))
        maze.blit(self.angle_frame_4, (cell_size * 25, cell_size * 25))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 25))

    def make_24_line(self):
        maze.blit(self.wall_2, (0, cell_size * 26))

        maze.blit(self.frame_1, (cell_size * 4, cell_size * 26))
        maze.blit(self.frame_2, (cell_size * 5, cell_size * 26))

        maze.blit(self.frame_1, (cell_size * 22, cell_size * 26))
        maze.blit(self.frame_2, (cell_size * 23, cell_size * 26))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 26))

    def make_25_line(self):
        maze.blit(self.spicific_angle_3, (0, cell_size * 27))
        maze.blit(self.frame_4, (cell_size, cell_size * 27))
        maze.blit(self.angle_frame_2, (cell_size * 2, cell_size * 27))

        maze.blit(self.frame_1, (cell_size * 4, cell_size * 27))
        maze.blit(self.frame_2, (cell_size * 5, cell_size * 27))

        maze.blit(self.angle_frame_1, (cell_size * 7, cell_size * 27))
        maze.blit(self.angle_frame_2, (cell_size * 8, cell_size * 27))

        maze.blit(self.angle_frame_1, (cell_size * 10, cell_size * 27))
        for i in range(1, 7):
            maze.blit(self.frame_3, (cell_size * (10 + i), cell_size * 27))
        maze.blit(self.angle_frame_2, (cell_size * 17, cell_size * 27))

        maze.blit(self.angle_frame_1, (cell_size * 19, cell_size * 27))
        maze.blit(self.angle_frame_2, (cell_size * 20, cell_size * 27))

        maze.blit(self.frame_1, (cell_size * 22, cell_size * 27))
        maze.blit(self.frame_2, (cell_size * 23, cell_size * 27))

        maze.blit(self.angle_frame_1, (cell_size * 25, cell_size * 27))
        maze.blit(self.frame_4, (cell_size * 26, cell_size * 27))
        maze.blit(self.spicific_angle_4, (cell_size * 27, cell_size * 27))

    def make_26_line(self):
        maze.blit(self.spicific_angle_5, (0, cell_size * 28))
        maze.blit(self.frame_3, (cell_size, cell_size * 28))
        maze.blit(self.angle_frame_4, (cell_size * 2, cell_size * 28))

        maze.blit(self.angle_frame_3, (cell_size * 4, cell_size * 28))
        maze.blit(self.angle_frame_4, (cell_size * 5, cell_size * 28))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 28))
        maze.blit(self.frame_2, (cell_size * 8, cell_size * 28))

        maze.blit(self.angle_frame_3, (cell_size * 10, cell_size * 28))
        for i in range(1, 7):
            maze.blit(self.frame_4, (cell_size * (10 + i), cell_size * 28))
        maze.blit(self.angle_frame_2, (cell_size * 13, cell_size * 28))
        maze.blit(self.angle_frame_1, (cell_size * 14, cell_size * 28))
        maze.blit(self.angle_frame_4, (cell_size * 17, cell_size * 28))

        maze.blit(self.frame_1, (cell_size * 19, cell_size * 28))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 28))

        maze.blit(self.angle_frame_3, (cell_size * 22, cell_size * 28))
        maze.blit(self.angle_frame_4, (cell_size * 23, cell_size * 28))

        maze.blit(self.angle_frame_3, (cell_size * 25, cell_size * 28))
        maze.blit(self.frame_3, (cell_size * 26, cell_size * 28))
        maze.blit(self.spicific_angle_6, (cell_size * 27, cell_size * 28))

    def make_27_line(self):
        maze.blit(self.wall_2, (0, cell_size * 29))

        maze.blit(self.frame_1, (cell_size * 7, cell_size * 29))
        maze.blit(self.frame_2, (cell_size * 8, cell_size * 29))

        maze.blit(self.frame_1, (cell_size * 13, cell_size * 29))
        maze.blit(self.frame_2, (cell_size * 14, cell_size * 29))

        maze.blit(self.frame_1, (cell_size * 19, cell_size * 29))
        maze.blit(self.frame_2, (cell_size * 20, cell_size * 29))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 29))

    def make_28_line(self):
        maze.blit(self.wall_2, (0, cell_size * 30))

        maze.blit(self.angle_frame_1, (cell_size * 2, cell_size * 30))
        for i in range(1, 5):
            maze.blit(self.frame_3, (cell_size * (2 + i), cell_size * 30))
        maze.blit(self.angle_frame_4, (cell_size * 7, cell_size * 30))
        maze.blit(self.angle_frame_3, (cell_size * 8, cell_size * 30))
        maze.blit(self.frame_3, (cell_size * 9, cell_size * 30))
        maze.blit(self.frame_3, (cell_size * 10, cell_size * 30))
        maze.blit(self.angle_frame_2, (cell_size * 11, cell_size * 30))

        maze.blit(self.frame_1, (cell_size * 13, cell_size * 30))
        maze.blit(self.frame_2, (cell_size * 14, cell_size * 30))

        maze.blit(self.angle_frame_1, (cell_size * 16, cell_size * 30))
        maze.blit(self.frame_3, (cell_size * 17, cell_size * 30))
        maze.blit(self.frame_3, (cell_size * 18, cell_size * 30))
        maze.blit(self.angle_frame_4, (cell_size * 19, cell_size * 30))
        maze.blit(self.angle_frame_3, (cell_size * 20, cell_size * 30))
        for i in range(1, 5):
            maze.blit(self.frame_3, (cell_size * (20 + i), cell_size * 30))
        maze.blit(self.angle_frame_2, (cell_size * 25, cell_size * 30))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 30))

    def make_29_line(self):
        maze.blit(self.wall_2, (0, cell_size * 31))

        maze.blit(self.angle_frame_3, (cell_size * 2, cell_size * 31))
        for i in range(1, 9):
            maze.blit(self.frame_4, (cell_size * (2 + i), cell_size * 31))
        maze.blit(self.angle_frame_4, (cell_size * 11, cell_size * 31))

        maze.blit(self.angle_frame_3, (cell_size * 13, cell_size * 31))
        maze.blit(self.angle_frame_4, (cell_size * 14, cell_size * 31))

        maze.blit(self.angle_frame_3, (cell_size * 16, cell_size * 31))
        for i in range(1, 9):
            maze.blit(self.frame_4, (cell_size * (16 + i), cell_size * 31))
        maze.blit(self.angle_frame_4, (cell_size * 25, cell_size * 31))

        maze.blit(self.wall_3, (cell_size * 27, cell_size * 31))

    def make_30_line(self):
        maze.blit(self.wall_2, (0, cell_size * 32))
        maze.blit(self.wall_3, (cell_size * 27, cell_size * 32))

    def make_31_line(self):
        maze.blit(self.angle_3, (0, cell_size * 33))
        for i in range(1, 27):
            maze.blit(self.wall_4, (cell_size * i, cell_size * 33))
        maze.blit(self.angle_4, (cell_size * 27, cell_size * 33))


def load_image(name, color_key=None, size=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (45, 45) if not size else size)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Ghost:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.animation = [load_image('data/ghosts/blinky/right1.png')]
        self.rect = self.animation[0].get_rect()
        self.mask = pygame.mask.from_surface(self.animation[0])
        self.rect.x = self.x
        self.rect.y = self.y

        self.counter = 0
        self.path = None

        self.last_seconds = 0

        self.angry = False  # злой режим для Блинки
        self.scatter = True  # режим разбегания
        self.in_the_game = False

    def update_time(self):
        self.last_seconds = seconds

    def pave(self, end=None):
        global disarming
        coord_y = int((self.y + 11 - 3 * cell_size) // cell_size)
        coord_x = int((self.x + 11) // cell_size)
        try:
            if self.counter == 0:
                if not self.scatter and (
                    not self.path or ((coord_x, coord_y) in important_points and not disarming)
                ):
                    if (int((end[1] + 11 - 3 * cell_size) // cell_size) < 0 or
                            int((end[0] + 11) // cell_size) < 0):
                        raise IndexError
                    pre_path = find_path(
                        nodes_matrix[coord_y][coord_x],
                        nodes_matrix[int((end[1] + 11 - 3 * cell_size) // cell_size)]
                        [int((end[0] + 11) // cell_size)])
                    if pre_path:
                        self.path = iter(pre_path)
                self.direction = next(self.path)
                in_the_passage = (coord_y == 14 and coord_x in [0, 1, 2, 3, 4, 5, 22, 23, 24, 25, 26, 27])
                self.counter = (8 if self.angry else 12) if not disarming and not in_the_passage else 16
                self.speed = (3 if self.angry else 2) if not disarming and not in_the_passage else 1.5
            self.x = round(self.x + self.direction[0] * self.speed, 1)
            self.y = round(self.y + self.direction[1] * self.speed, 1)
            self.rect.x = self.x
            self.rect.y = self.y
            self.counter -= 1
        except StopIteration:
            self.path = None
        except TypeError:
            self.path = None
        except IndexError:
            if isinstance(self, Pinky):
                self.pave((pacman.x, pacman.y))
            elif isinstance(self, Inky):
                path_x, path_y = pacman.x - 2 * cell_size, pacman.y - 2 * cell_size
                if int((path_x + 11) // cell_size) > 0 and int((path_y + 11 - 3 * cell_size) // cell_size) > 0:
                    self.pave((path_x, path_y))
                else:
                    self.pave((pacman.x, pacman.y))

        if disarming:
            if self.last_seconds == 0:
                self.update_time()

            up_time = 10 - level // 2
            time_shift = round(up_time - (seconds - self.last_seconds), 2)
            if time_shift == 0:
                disarming = False
                self.last_seconds = 0
            elif time_shift in [3.3, 2.65, 1.98, 1.32, 0.65]:
                self.animation = [load_image('data/ghosts/killing/end-disarmed1.png'),
                                  load_image('data/ghosts/killing/end-disarmed2.png')]
            elif time_shift in [2.97, 2.32, 1.65, 0.98, 0.33] or up_time - 0.05 <= time_shift <= up_time:
                self.animation = [load_image('data/ghosts/killing/disarmed1.png'),
                                  load_image('data/ghosts/killing/disarmed2.png')]


class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.animation = [load_image('data/ghosts/blinky/right1.png'), load_image('data/ghosts/blinky/right2.png')]
        self.start_dispersion((14, 11))
        self.scatter = True

    def start_dispersion(self, end):
        self.path = iter(find_path(nodes_matrix[end[1]][end[0]], nodes_matrix[1][25]) + [(1, 0)])

    def move(self, type_of_move='normal'):
        if type_of_move == 'agressive':
            self.angry = True
        elif type_of_move == 'normal':
            self.angry = False

        coord_x = int((self.x + 11) // cell_size)
        coord_y = int((self.y + 11 - 3 * cell_size) // cell_size)
        
        if disarming and not self.path:
            diff_x, diff_y = pacman.x - self.x, pacman.y - self.y
            if 1 <= diff_x <= 48 and 1 <= diff_y <= 48:
                super().pave((self.x - diff_x, self.y - diff_y))
            else:
                pacman_x = int((pacman.x + 11) // cell_size)
                pacman_y = int((pacman.y + 11 - 3 * cell_size) // cell_size)
                try:
                    direct = find_path(nodes_matrix[coord_y][coord_x], nodes_matrix[pacman_y][pacman_x])[0]
                except Exception:
                    direct = None
                good_directions = {(-1, 0), (1, 0), (0, 1), (0, -1)} - {direct}
                free_directions = []
                for dir_ in good_directions:
                    try:
                        if nodes_matrix[coord_y + dir_[1]][coord_x + dir_[0]].type != 'wall':
                            free_directions.append(dir_)
                    except IndexError:
                        pass
                if direct:
                    self.path = iter([random.choice(free_directions) if free_directions else direct])
                else:
                    self.path = iter([self.direction] * 7)
                super().pave()
        elif (coord_x, coord_y) == (5, 14) and self.direction == (-1, 0):
            self.path = iter([(-1, 0)] * 6)
            super().pave()
        elif (coord_x, coord_y) == (-1, 14) and self.direction == (-1, 0):
            self.x = 28 * cell_size - 12
            self.rect.x = self.x
        elif (coord_x, coord_y) == (22, 14) and self.direction == (1, 0):
            self.path = iter([(1, 0)] * 6)
            super().pave()
        elif (coord_x, coord_y) == (28, 14) and self.direction == (1, 0):
            self.x = -1 * cell_size - 10
            self.rect.x = self.x
        elif self.scatter:
            if (coord_x, coord_y) != (14, 11) and not self.path:
                self.start_dispersion((coord_x, coord_y))
            elif (coord_x, coord_y) == (22, 5):
                self.path = iter(find_path(nodes_matrix[5][22], nodes_matrix[1][24]) + [(1, 0)] * 2)
            elif (coord_x, coord_y) == (26, 1):
                self.path = iter(find_path(nodes_matrix[1][26], nodes_matrix[5][23])[1:] + [(-1, 0)])
            super().pave()
        elif not self.path:
            super().pave((pacman.x, pacman.y))
        else:
            super().pave()
            
        if self.direction == (1, 0):
            side = 'right'
        elif self.direction == (-1, 0):
            side = 'left'
        elif self.direction == (0, 1):
            side = 'down'
        elif self.direction == (0, -1):
            side = 'up'

        if not disarming:
            angry = 'angry_' if self.angry else ''
            self.animation = [load_image('data/ghosts/blinky/{}{}1.png'.format(angry, side)),
                              load_image('data/ghosts/blinky/{}{}2.png'.format(angry, side))]


class Pinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.animation = [load_image('data/ghosts/pinky/right1.png'), load_image('data/ghosts/pinky/right2.png')]
        self.angry = True if level == 16 else False

    def start_dispersion(self, end):
        self.path = iter(find_path(nodes_matrix[end[1]][end[0]], nodes_matrix[1][1]))

    def move(self):
        coord_y = int((self.y + 11 - 3 * cell_size) // cell_size)
        coord_x = int((self.x + 11) // cell_size)
        
        if not self.in_the_game and not self.path:
            self.path = iter([(0, 1), (0, 1), (0, -1), (0, -1)])
            super().pave()
        elif disarming and not self.path:
            diff_x, diff_y = pacman.x - self.x, pacman.y - self.y
            if 1 <= diff_x <= 48 and 1 <= diff_y <= 48:
                super().pave((self.x - diff_x, self.y - diff_y))
            else:
                pacman_x = int((pacman.x + 11) // cell_size)
                pacman_y = int((pacman.y + 11 - 3 * cell_size) // cell_size)
                try:
                    direct = find_path(nodes_matrix[coord_y][coord_x], nodes_matrix[pacman_y][pacman_x])[0]
                except Exception:
                    direct = None
                good_directions = {(-1, 0), (1, 0), (0, 1), (0, -1)} - {direct}
                free_directions = []
                for dir_ in good_directions:
                    try:
                        if nodes_matrix[coord_y + dir_[1]][coord_x + dir_[0]].type != 'wall':
                            free_directions.append(dir_)
                    except IndexError:
                        pass
                if direct:
                    self.path = iter([random.choice(free_directions) if free_directions else direct])
                else:
                    self.path = iter([self.direction] * 7)
                super().pave()
        elif (coord_x, coord_y) == (5, 14) and self.direction == (-1, 0):
            self.path = iter([(-1, 0)] * 6)
            super().pave()
        elif (coord_x, coord_y) == (-1, 14) and self.direction == (-1, 0):
            self.x = 28 * cell_size - 12
            self.rect.x = self.x
        elif (coord_x, coord_y) == (22, 14) and self.direction == (1, 0):
            self.path = iter([(1, 0)] * 6)
            super().pave()
        elif (coord_x, coord_y) == (28, 14) and self.direction == (1, 0):
            self.x = -1 * cell_size - 10
            self.rect.x = self.x
        elif self.scatter:
            if (coord_x, coord_y) == (6, 5):
                self.path = iter(find_path(nodes_matrix[5][6], nodes_matrix[1][2]) + [(-1, 0)])
            elif (coord_x, coord_y) == (1, 1):
                self.path = iter(find_path(nodes_matrix[1][1], nodes_matrix[5][6])[1:])
            elif not self.path:
                self.start_dispersion((coord_x, coord_y))
            super().pave()
        elif not self.path:
            super().pave(
                (pacman.x + pacman.direction[0] * cell_size * 4, pacman.y + pacman.direction[1] * cell_size * 4))
        else:
            super().pave()

        if self.direction == (1, 0):
            self.side = 'right'
        elif self.direction == (-1, 0):
            self.side = 'left'
        elif self.direction == (0, 1):
            self.side = 'down'
        elif self.direction == (0, -1):
            self.side = 'up'

        if not disarming:
            self.animation = [load_image('data/ghosts/pinky/{}1.png'.format(self.side)),
                              load_image('data/ghosts/pinky/{}2.png'.format(self.side))]


class Inky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.animation = [load_image('data/ghosts/inky/right1.png'), load_image('data/ghosts/inky/right2.png')]
        self.angry = True if level >= 14 else False

    def start_dispersion(self, end):
        self.path = iter(find_path(nodes_matrix[end[1]][end[0]], nodes_matrix[23][21]))

    def move(self):
        coord_y = int((self.y + 11 - 3 * cell_size) // cell_size)
        coord_x = int((self.x + 11) // cell_size)
        
        if not self.in_the_game and not self.path:
            self.path = iter([(0, -1), (0, -1), (0, 1), (0, 1)])
            super().pave()
        elif disarming and not self.path:
            diff_x, diff_y = pacman.x - self.x, pacman.y - self.y
            if 1 <= diff_x <= 48 and 1 <= diff_y <= 48:
                super().pave((self.x - diff_x, self.y - diff_y))
            else:
                pacman_x = int((pacman.x + 11) // cell_size)
                pacman_y = int((pacman.y + 11 - 3 * cell_size) // cell_size)
                try:
                    direct = find_path(nodes_matrix[coord_y][coord_x], nodes_matrix[pacman_y][pacman_x])[0]
                except Exception:
                    direct = None
                good_directions = {(-1, 0), (1, 0), (0, 1), (0, -1)} - {direct}
                free_directions = []
                for dir_ in good_directions:
                    try:
                        if nodes_matrix[coord_y + dir_[1]][coord_x + dir_[0]].type != 'wall':
                            free_directions.append(dir_)
                    except IndexError:
                        pass
                if direct:
                    self.path = iter([random.choice(free_directions) if free_directions else direct])
                else:
                    self.path = iter([self.direction] * 7)
                super().pave()
        elif (coord_x, coord_y) == (5, 14) and self.direction == (-1, 0):
            self.path = iter([(-1, 0)] * 6)
            super().pave()
        elif (coord_x, coord_y) == (-1, 14) and self.direction == (-1, 0):
            self.x = 28 * cell_size - 12
            self.rect.x = self.x
        elif (coord_x, coord_y) == (22, 14) and self.direction == (1, 0):
            self.path = iter([(1, 0)] * 6)
            super().pave()
        elif (coord_x, coord_y) == (28, 14) and self.direction == (1, 0):
            self.x = -1 * cell_size - 10
            self.rect.x = self.x
        elif self.scatter:
            if (coord_x, coord_y) == (21, 23):
                self.path = iter(find_path(nodes_matrix[23][21], nodes_matrix[29][22])[1:] + [(-1, 0)] * 3)
            elif (coord_x, coord_y) == (19, 29):
                self.path = iter(find_path(nodes_matrix[29][19], nodes_matrix[23][21]))
            elif not self.path:
                self.start_dispersion((coord_x, coord_y))
            super().pave()
        elif not self.path:
            pacman_x = pacman.x + pacman.direction[0] * cell_size * 2
            pacman_y = pacman.y + pacman.direction[1] * cell_size * 2
            super().pave((blinky.x + (pacman_x - blinky.x) * 2, blinky.y + (pacman_y - blinky.y) * 2))
        else:
            super().pave()

        if self.direction == (1, 0):
            self.side = 'right'
        elif self.direction == (-1, 0):
            self.side = 'left'
        elif self.direction == (0, 1):
            self.side = 'down'
        elif self.direction == (0, -1):
            self.side = 'up'

        if not disarming:
            self.animation = [load_image('data/ghosts/inky/{}1.png'.format(self.side)),
                              load_image('data/ghosts/inky/{}2.png'.format(self.side))]


class Clyde(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.animation = [load_image('data/ghosts/clyde/right1.png'), load_image('data/ghosts/clyde/right2.png')]
        self.angry = True if level >= 12 else False
        self.false_scatter = False

    def start_dispersion(self, end):
        self.path = iter(find_path(nodes_matrix[end[1]][end[0]], nodes_matrix[23][7]))

    def move(self):
        coord_y = int((self.y + 11 - 3 * cell_size) // cell_size)
        coord_x = int((self.x + 11) // cell_size)
        pacman_y = int((pacman.y + 11 - 3 * cell_size) // cell_size)
        pacman_x = int((pacman.x + 11) // cell_size)
        path_to_pacman = find_path(nodes_matrix[coord_y][coord_x], nodes_matrix[pacman_y][pacman_x])
        length_to_pacman = len(path_to_pacman) if path_to_pacman else 1
        
        if not self.in_the_game and not self.path:
            self.path = iter([(0, -1), (0, -1), (0, 1), (0, 1)])
            super().pave()
        elif disarming and not self.path:
            diff_x, diff_y = pacman.x - self.x, pacman.y - self.y
            if 1 <= diff_x <= 48 and 1 <= diff_y <= 48:
                super().pave((self.x - diff_x, self.y - diff_y))
            else:
                try:
                    direct = find_path(nodes_matrix[coord_y][coord_x], nodes_matrix[pacman_y][pacman_x])[0]
                except Exception:
                    direct = None
                good_directions = {(-1, 0), (1, 0), (0, 1), (0, -1)} - {direct}
                free_directions = []
                for dir_ in good_directions:
                    try:
                        if nodes_matrix[coord_y + dir_[1]][coord_x + dir_[0]].type != 'wall':
                            free_directions.append(dir_)
                    except IndexError:
                        pass
                if direct:
                    self.path = iter([random.choice(free_directions) if free_directions else direct])
                else:
                    self.path = iter([self.direction] * 7)
                super().pave()
        elif (coord_x, coord_y) == (5, 14) and self.direction == (-1, 0):
            self.path = iter([(-1, 0)] * 6)
            super().pave()
        elif (coord_x, coord_y) == (-1, 14) and self.direction == (-1, 0):
            self.x = 28 * cell_size - 12
            self.rect.x = self.x
        elif (coord_x, coord_y) == (22, 14) and self.direction == (1, 0):
            self.path = iter([(1, 0)] * 6)
            super().pave()
        elif (coord_x, coord_y) == (28, 14) and self.direction == (1, 0):
            self.x = -1 * cell_size - 10
            self.rect.x = self.x
        elif self.scatter or self.false_scatter:
            if self.false_scatter and length_to_pacman > 8:
                self.false_scatter = False
                self.scatter = False

            if (coord_x, coord_y) == (7, 23):
                self.path = iter(find_path(nodes_matrix[23][7], nodes_matrix[29][5]) + [(1, 0)] * 2)
            elif (coord_x, coord_y) == (7, 29):
                self.path = iter(find_path(nodes_matrix[29][7], nodes_matrix[23][7])[1:])
            elif not self.path:
                self.start_dispersion((coord_x, coord_y))

            super().pave()
        elif not self.path:
            if length_to_pacman <= 8:
                self.false_scatter = True
                self.scatter = True
            else:
                super().pave((pacman.x, pacman.y))
        else:
            super().pave()

        if self.direction == (1, 0):
            self.side = 'right'
        elif self.direction == (-1, 0):
            self.side = 'left'
        elif self.direction == (0, 1):
            self.side = 'down'
        elif self.direction == (0, -1):
            self.side = 'up'

        if not disarming:
            self.animation = [load_image('data/ghosts/clyde/{}1.png'.format(self.side)),
                              load_image('data/ghosts/clyde/{}2.png'.format(self.side))]


class Pac_man:
    def __init__(self, x, y, direction):
        self.x, self.y = x, y
        self.frame = 0

        self.animation = \
            {
                (0, 0): [load_image('data/pacman/full.png')] * 3,
                (-1, 0): [load_image('data/pacman/left1.png', -1),
                          load_image('data/pacman/left2.png', -1),
                          load_image('data/pacman/full.png')],
                (1, 0): [load_image('data/pacman/right1.png', -1),
                         load_image('data/pacman/right2.png', -1),
                         load_image('data/pacman/full.png')],
                (0, -1): [load_image('data/pacman/up1.png', -1),
                          load_image('data/pacman/up2.png', -1),
                          load_image('data/pacman/full.png')],
                (0, 1): [load_image('data/pacman/down1.png', -1),
                         load_image('data/pacman/down2.png', -1),
                         load_image('data/pacman/full.png')]
            }

        self.speed = 1
        self.direction = direction  # это то направление в которое двигается pacman в данный момент
        self.player_direction = (0, 0)  # направление, куда хочет двигаться игрок

        self.rect = self.animation[self.direction][0].get_rect()
        self.mask = pygame.mask.from_surface(self.animation[self.direction][0])
        self.rect.x = self.x
        self.rect.y = self.y

        self.path = [int((self.y + 11 - 3 * cell_size) // cell_size), int((self.x + 11) // cell_size)]

    def move(self):
        if self.wall_check(self.player_direction):
            self.direction = self.player_direction

        if self.wall_check(self.direction):
            if self.direction == (-1, 0) or self.direction == (0, -1):
                self.path = [int((self.y + 32 - 3 * cell_size) // cell_size), int((self.x + 32) // cell_size)]
            else:
                self.path = [int((self.y + 11 - 3 * cell_size) // cell_size), int((self.x + 11) // cell_size)]

            self.x += (self.speed * self.direction[0])
            self.y += (self.speed * self.direction[1])
            self.rect.x = self.x
            self.rect.y = self.y

            if self.x <= 0:
                self.x = 671
            if self.x >= 672:
                self.x = 0

    def wall_check(self, direction):  # 1. Есть ли стена 2. Можно ли ещё пододвинуться к стенке 3. Направление
        try:
            if nodes_matrix[self.path[0]][self.path[1] - 1].type == 'wall' and \
                    cell_size * self.path[1] - 10 >= self.x and \
                    direction[0] == -1:
                return False

            if nodes_matrix[self.path[0]][self.path[1] + 1].type == 'wall' and \
                    cell_size * self.path[1] - 10 <= self.x and \
                    direction[0] == 1:
                return False

            if nodes_matrix[self.path[0] - 1][self.path[1]].type == 'wall' and \
                    cell_size * (self.path[0] + 3) - 10 >= self.y and \
                    direction[1] == -1:
                return False

            if nodes_matrix[self.path[0] + 1][self.path[1]].type == 'wall' and \
                    cell_size * (self.path[0] + 3) - 10 <= self.y and \
                    direction[1] == 1:
                return False
        except IndexError:
            return True
        return True

    def frames(self):
        if self.wall_check(self.direction):
            if global_frame % 4 == 0:
                self.frame += 1


class TotalPoints:
    def __init__(self):
        self.points = 0
        self.lifes = 3
        self.fruits = 0
        self.last_ten_thousand = 0
        with open('scores.txt', 'r') as file:
            string = file.readline()
            if string:
                if ',' in string:
                    scores = list(map(int, string.split(', ')))
                else:
                    scores = [int(string)]
            else:
                scores = [0]
        scores = sorted(scores)[::-1]
        self.high_score = str(scores[0]) if scores[0] < 999999 else '999999'
    
    def increase_points(self, num):
        self.points += num
        if self.points // 10000 != self.last_ten_thousand:
            self.lifes += 1 if self.lifes < 5 else 0
            self.last_ten_thousand = self.points // 10000
    
    def eat_fruit(self):
        if self.next_by_order == 'cherry':
            self.points += 100
        elif self.next_by_order == 'strawberry':
            self.points += 300
        elif self.next_by_order == 'peach':
            self.points += 500
        elif self.next_by_order == 'apple':
            self.points += 700
        elif self.next_by_order == 'melon':
            self.points += 1000
        elif self.next_by_order == 'spaceship':
            self.points += 2000
        elif self.next_by_order == 'bell':
            self.points += 3000
        elif self.next_by_order == 'key':
            self.points += 5000
            
        if self.points // 10000 != self.last_ten_thousand:
            self.lifes += 1 if self.lifes < 5 else 0
            self.last_ten_thousand = self.points // 10000
        
        self.fruits += 1 if self.fruits < len(fruits_order) - 1 else 0
    
    def show_fruit(self):
        if self.fruits + 1 < len(fruits_order):
            self.next_by_order = fruits_order[self.fruits + 1][-1]
        fruits_to_show = fruits_order[self.fruits]
        return (fruits_to_show, self.next_by_order)


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.x, self.y = x, y
        self.eaten = False

    def update(self, *args):
        if pygame.sprite.collide_mask(self, pacman) and not self.eaten:
            self.eaten = True
            points_sprite.remove(self)
            totalpoints.increase_points(10)


class Point(Object, pygame.sprite.Sprite):
    image = load_image('data/other/s_food.png', -1, (cell_size, cell_size))

    def __init__(self, x, y):
        super().__init__(x, y, points_sprite)
        self.image = Point.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        points_sprite.add(self)


class Energizer(Object, pygame.sprite.Sprite):
    image = load_image('data/other/b_food.png', -1, (cell_size, cell_size))

    def __init__(self, x, y):
        super().__init__(x, y, points_sprite)
        self.image = Energizer.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        points_sprite.add(self)

    def update(self, ghosts):
        global disarming
        if global_frame % 20 in range(10):
            pygame.draw.rect(screen, '#000000', self.rect)
        if pygame.sprite.collide_mask(self, pacman) and not self.eaten:
            totalpoints.increase_points(50)
            for g in ghosts:
                g.update_time()
                if g.in_the_game:
                    g.path = None
            disarming = True
            super().update()


class Fruit(Object):
    def __init__(self, x, y):
        super().__init__(x, y)


def render_counters():
    font = pygame.font.Font('data/PacMan Font.ttf', 24)
    text = font.render('1UP', True, '#dedeff')
    text_x, text_y = 72, 0
    screen.blit(text, (text_x, text_y))
    text = font.render('HIGH', True, '#dedeff')
    text_x, text_y = 216, 0
    screen.blit(text, (text_x, text_y))
    text = font.render('SCORE', True, '#dedeff')
    text_x, text_y = 336, 0
    screen.blit(text, (text_x, text_y))
    text = font.render('0' * (6 - len(str(totalpoints.points))) + str(totalpoints.points), True, '#dedeff')
    if totalpoints.points > 999999:
        text = font.render('999999', True, '#dedeff')
    text_x, text_y = 24, 24
    screen.blit(text, (text_x, text_y))
    text = font.render('0' * (6 - len(str(totalpoints.high_score))) + str(totalpoints.high_score), True, '#dedeff')
    text_x, text_y = 264, 24
    screen.blit(text, (text_x, text_y))
    
    life = load_image('data/other/life.png')
    for i in range(totalpoints.lifes - 1):
        screen.blit(life, (16 + 45 * i, 34 * cell_size))
    
    fruits = totalpoints.show_fruit()[0]
    for i in range(len(fruits)):
        fimage = load_image('data/fruits/{}.png'.format(fruits[i]))
        screen.blit(fimage, (26 * cell_size - 16 - 45 * i, 34 * cell_size))


def make_game(lvl, restart=False):
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/game_start.wav'))
    global screen, pacman, points_sprite, global_frame, blinky, level, seconds, disarming, food
    fps = 60
    running, paused = True, False
    disarming, win = False, False

    # данные на вывод
    level, seconds = lvl, 0

    if not restart:
        points_sprite = pygame.sprite.Group()
        food = []

        for line in nodes_matrix:
            for cell in line:
                if cell.has_food:
                    food.append(Point(cell.x * cell_size, cell.y * cell_size + 3 * cell_size))
                elif cell.has_energy:
                    food.append(Energizer(cell.x * cell_size, cell.y * cell_size + 3 * cell_size))

    pacman = Pac_man(cell_size * 14 - 11, cell_size * 26 - 11, (0, 0))
    blinky = Blinky(cell_size * 14 - 11, cell_size * 11 - 11 + 3 * cell_size)
    pinky = Pinky(cell_size * 13.5 - 11, cell_size * 13 - 11 + 3 * cell_size)
    inky = Inky(cell_size * 11.5 - 11, cell_size * 15 - 11 + 3 * cell_size)
    clyde = Clyde(cell_size * 15.5 - 11, cell_size * 15 - 11 + 3 * cell_size)
    points_sprite.draw(screen)

    clock = pygame.time.Clock()
    global_frame, frame, sound_frame, clear_frame = 0, 0, 0, fps * 7 - 1 if restart else 0

    screen.fill((0, 0, 0))
    ex = Field()
    ex.update()
    font = pygame.font.Font('data/PacMan Font.ttf', 25 if level != 16 else 20)

    text = font.render("LEVEL  {}".format(lvl) if level != 16 else 'LAST LEVEL 16', True, '#ffcc00')
    text_x = size[0] // 2 - text.get_width() // 2
    text_y = size[1] // 2 - text.get_height() // 2 + 60
    screen.blit(text, (text_x, text_y))
    render_counters()
    pygame.display.flip()
    sleep(3.17)
    ex.update()

    text = font.render("READY!", True, '#ffcc00')
    text_x = size[0] // 2 - text.get_width() // 2
    text_y = size[1] // 2 - text.get_height() // 2 + 60
    screen.blit(text, (text_x, text_y))
    render_counters()
    pygame.display.flip()
    sleep(0.266)
    ex.update()

    text = font.render("SET!", True, '#ffcc00')
    text_x = size[0] // 2 - text.get_width() // 2
    text_y = size[1] // 2 - text.get_height() // 2 + 60
    screen.blit(text, (text_x, text_y))
    render_counters()
    pygame.display.flip()
    sleep(0.266)
    ex.update()

    text = font.render("PLAY!", True, '#ffcc00')
    text_x = size[0] // 2 - text.get_width() // 2
    text_y = size[1] // 2 - text.get_height() // 2 + 60
    screen.blit(text, (text_x, text_y))
    render_counters()
    pygame.display.flip()
    sleep(0.4)
    pygame.mixer.Channel(1).set_volume(0.5)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/siren_1.wav'), 10000)

    while running:
        ex.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    pacman.player_direction = (-1, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    pacman.player_direction = (1, 0)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    pacman.player_direction = (0, -1)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    pacman.player_direction = (0, 1)
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_SPACE:
                    totalpoints.eat_fruit()

        if global_frame % 4 == 0:
            frame += 1
            
        points_sprite.draw(screen)
        
        for f in food:
            if pygame.sprite.collide_mask(f, pacman) and not f.eaten and (global_frame - sound_frame) > 15:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/wakka.wav'))
                pygame.mixer.Channel(0).set_volume(0.8)
                sound_frame = global_frame
            f.update([blinky, pinky, inky, clyde])
        
        screen.blit(pacman.animation[pacman.direction][pacman.frame % 3], (pacman.x, pacman.y))
        screen.blit(blinky.animation[frame % 2], (blinky.x, blinky.y))
        screen.blit(pinky.animation[frame % 2], (pinky.x, pinky.y))
        screen.blit(inky.animation[frame % 2], (inky.x, inky.y))
        screen.blit(clyde.animation[frame % 2], (clyde.x, clyde.y))
        
        if not paused:
            pygame.mixer.Channel(1).set_volume(0.5)
            global_frame += 1
            clear_frame += 1 if not disarming else 0
            seconds = global_frame / fps
            clear_seconds = clear_frame / fps
            
            
            for _ in range(3):
                pacman.move()
            pacman.frames()
            blinky.move('agressive' if len(points_sprite.sprites()) <= 20 + level * 14 else 'normal')
            pinky.move()
            inky.move()
            clyde.move()
            
            sl = (len(food) - len(points_sprite.sprites())) // 49 + 1 if not disarming else -1
            raw = pygame.mixer.Channel(1).get_sound().get_raw()
            if disarming and (raw[12], raw[16]) != (254, 2):
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/active_energy.wav'), 10000)
            if sl == 2 and (raw[12], raw[16]) != (0, 0):
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/siren_2.wav'), 10000)
            elif sl == 3 and (raw[12], raw[16]) != (253, 4):
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/siren_3.wav'), 10000)
            elif sl == 4 and (raw[12], raw[16]) != (255, 2):
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/siren_4.wav'), 10000)
            elif sl == 5 and (raw[12], raw[16]) != (254, 1):
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/siren_5.wav'), 10000)

            if clear_seconds >= 7 - level * 0.4375 and not pinky.in_the_game and not disarming:
                pinky.path = iter([(0, -1)] * 3 + [(0.5, 0)])
                pinky.in_the_game = True
            if len(food) - len(points_sprite.sprites()) >= (54 - 4 * level) and not inky.in_the_game and not disarming:
                inky.path = iter([(1, 0)] * 2 + [(0, -1)] * 3 + [(0.5, 0)])
                inky.in_the_game = True
            if len(food) - len(points_sprite.sprites()) >= (96 - 6 * level) and not clyde.in_the_game and not disarming:
                clyde.path = iter([(-1, 0)] * 1 + [(0, -1)] * 3 + [(0.5, 0)])
                clyde.in_the_game = True

            if clear_seconds == 7:
                for ghost in (blinky, pinky, inky, clyde):
                    ghost.scatter = False
            if clear_seconds == 27:
                for ghost in (blinky, pinky, inky, clyde):
                    ghost.scatter = True
            if clear_seconds == 34 - 2 * (level >= 4) - 2 * (level >= 10):
                for ghost in (blinky, pinky, inky, clyde):
                    ghost.scatter = False
            if clear_seconds == 54 - 2 * (level >= 4) - 2 * (level >= 10):
                for ghost in (blinky, pinky, inky, clyde):
                    ghost.scatter = True
            if clear_seconds == 59 - 4 * (level >= 4) - 4 * (level >= 10):
                for ghost in (blinky, pinky, inky, clyde):
                    ghost.scatter = False
            if clear_seconds == 79 + 4 * (level >= 4) + 4 * (level >= 10):
                for ghost in (blinky, pinky, inky, clyde):
                    ghost.scatter = True
            if clear_seconds == 84 + 4 * (level >= 4) + 4 * (level >= 10):
                for ghost in (blinky, pinky, inky, clyde):
                    ghost.scatter = False
        else:
            pygame.mixer.Channel(1).set_volume(0)
            blured = pygame.transform.smoothscale(screen, (63, 81))
            blured = pygame.transform.smoothscale(blured, size)
            dark = pygame.Surface(size)
            pygame.draw.rect(dark, (0, 0, 0), (0, 0, size[0], size[1]))
            dark.set_alpha(80)
            blured.blit(dark, (0, 0))
            screen.blit(blured, (0, 0))
            
            font = pygame.font.Font('data/PacMan Font.ttf', 55)
            text = font.render("PAUSED", True, '#ffffff')
            text_x = size[0] // 2 - text.get_width() // 2
            text_y = size[1] // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))
        
        if not points_sprite.sprites():
            running = False
            win = True
        
        for ghost in [blinky, pinky, inky, clyde]:
            if pygame.sprite.collide_mask(pacman, ghost):
                if not disarming:
                    pygame.mixer.Channel(1).stop()
                    sleep(1)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/death.wav'), 1)
                    for i in range(1, 11):
                        screen.fill('#000000', (pacman.x, pacman.y, 45, 45))
                        screen.blit(load_image('data/pacman/die{}.png'.format(i)), (pacman.x, pacman.y))
                        render_counters()
                        pygame.display.flip()
                        sleep(0.1)
                    screen.fill('#000000', (pacman.x, pacman.y, 45, 45))
                    screen.blit(load_image('data/pacman/die11.png'), (pacman.x, pacman.y))
                    render_counters()
                    pygame.display.flip()
                    sleep(0.9)
                    
                    totalpoints.lifes -= 1
                    if totalpoints.lifes > 0:
                        make_game(level, restart=True)
                    else:
                        win, running = False, False
            
            
        render_counters()
        clock.tick(fps)
        pygame.display.flip()
        
    pygame.mixer.Channel(1).stop()

    if win:
        ex.update()
        render_counters()
        pygame.display.flip()
        sleep(2)

        if level != 16:
            phrases = ['GOOD   BOY!', 'PERFECT!', 'FANTASTIC!', 'WOW!  GREAT!', 'EXCELLENT!']
        else:
            phrases = ['YOU   WIN!']
        
        font = pygame.font.Font('data/PacMan Font.ttf', 25)
        text = font.render(random.choice(phrases), True, '#ffff00')
        text_x = size[0] // 2 - text.get_width() // 2
        text_y = size[1] // 2 - text.get_height() // 2 + 60
        screen.blit(text, (text_x, text_y))
        render_counters()
        pygame.display.flip()
        sleep(2.2)
        ex.update()
        with open('scores.txt', 'a') as file:
            with open('scores.txt', 'r') as test_file:
                if test_file.readlines():
                    file.write(', ' + str(totalpoints.points))
                else:
                    file.write(str(totalpoints.points))
        if level != 16:
            make_game(level + 1)
    else:
        ex.update()
        render_counters()
        pygame.display.flip()
        sleep(2)
        font = pygame.font.Font('data/PacMan Font.ttf', 25)
        text = font.render('GAME     OVER', True, '#ff0000')
        text_x = size[0] // 2 - text.get_width() // 2
        text_y = size[1] // 2 - text.get_height() // 2 + 60
        screen.blit(text, (text_x, text_y))
        render_counters()
        pygame.display.flip()
        sleep(2.2)
        ex.update()
        with open('scores.txt', 'a') as file:
            with open('scores.txt', 'r') as test_file:
                if test_file.readlines():
                    file.write(', ' + str(totalpoints.points))
                else:
                    file.write(str(totalpoints.points))
        exit()
        

if __name__ == '__main__':
    totalpoints = TotalPoints()
    pacman, points_sprite, global_frame, level, blinky, seconds, disarming, food = 0, 0, 0, 0, 0, 0, 0, 0
    pygame.mixer.init()

    font = pygame.font.Font('data/PacMan Font.ttf', 45)
    text = font.render("PAC- MAN", True, '#fdd700')
    screen.blit(text, ((size[0] - text.get_width()) // 2, 250))

    font = pygame.font.Font('data/PacMan Font.ttf', 15)    
    text = font.render("WASD   OR   ARROW   KEYS   TO   CONTROL", True, '#b69200')
    text_x = (size[0] - text.get_width()) // 2
    text_y = (size[1] - text.get_height()) // 2 + 95
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    
    text = font.render("P  -  PAUSE", True, '#b69200')
    text_x = (size[0] - text.get_width()) // 2
    text_y = (size[1] - text.get_height()) // 2 + 120
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    
    text = font.render("SMALL   POINT   -   10 PTS", True, '#b69200')
    text_x = (size[0] - text.get_width()) // 2
    text_y = (size[1] - text.get_height()) // 2 + 170
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    
    text = font.render("ENERGIZER   -   50 PTS", True, '#b69200')
    text_x = (size[0] - text.get_width()) // 2
    text_y = (size[1] - text.get_height()) // 2 + 195
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    
    text = font.render("BOUNS   PAC- MAN   FOR   10000 PTS", True, '#b69200')
    text_x = (size[0] - text.get_width()) // 2
    text_y = (size[1] - text.get_height()) // 2 + 220
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    
    text = font.render("BY   PAVEL   OVCHINNIKOV", True, '#00c800')
    text_x = (size[0] - text.get_width()) // 2
    text_y = (size[1] - text.get_height()) // 2 + 300
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))

    text = font.render("MARK   ERMOLAEV", True, '#00c800')
    text_x = (size[0] - text.get_width()) // 2
    text_y = (size[1] - text.get_height()) // 2 + 325
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))

    text = font.render("VALERIY   PROSHAK", True, '#00c800')
    text_x = (size[0] - text.get_width()) // 2
    text_y = (size[1] - text.get_height()) // 2 + 350
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    
    text = font.render("ALL   RIGHTS   RESERVED   BY", True, '#fdd700')
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = size[0] - text_w - 126
    text_y = size[1] - text_h - 8
    screen.blit(text, (text_x, text_y))
    logo_namco = load_image('data/Namco logo and colors.png', size=(106, 17))
    screen.blit(logo_namco, (size[0] - 114, size[1] - 10 - text_h))

    font = pygame.font.Font('data/PacMan Font.ttf', 25)
    text = font.render("TAP  TO   PLAY", True, '#ffcc00')
    text_x = size[0] // 2 - text.get_width() // 2
    text_y = size[1] // 2 - text.get_height() // 2 + 60
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))

    render_counters()
    pygame.display.flip()
    pygame.display.set_caption('PAC-MAN')
    
    clock = pygame.time.Clock()
    animation_frame = 0
    running = True
    cycle = [1, 2, 3, 2] * 10000
    
    while running:
        screen.fill((0, 0, 0), (272, 100, 128, 128))
        global_frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if (
                event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or
                event.type == pygame.MOUSEBUTTONDOWN and 
                -5 <= event.pos[0] - text_x <= text_w + 5 and -5 <= event.pos[1] - text_y <= text_h + 5
            ):
                font = pygame.font.Font('data/PacMan Font.ttf', 25)
                text = font.render("TAP  TO   PLAY", True, '#b69200')
                text_x = size[0] // 2 - text.get_width() // 2
                text_y = size[1] // 2 - text.get_height() // 2 + 60
                text_w = text.get_width()
                text_h = text.get_height()
                screen.blit(load_image(
                    'data/other/logo{}.png'.format(cycle[global_frame // 10]), size=(128, 128)
                ), (272, 100))
                screen.blit(text, (text_x, text_y))
                pygame.display.flip()
                sleep(0.5)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/any_button.wav'))
                running = False
        screen.blit(load_image('data/other/logo{}.png'.format(cycle[global_frame // 10]), size=(128, 128)), (272, 100))
        clock.tick(60)
        pygame.display.flip()
    make_game(1)


pygame.quit()

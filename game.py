import os
import pygame, pygame.display, pygame.sprite
from typing import List, Optional, Set, Tuple

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


def build_path(to_node: Cell) -> List[Tuple[int, int]]:
    global nodes_matrix
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


class Field:
    global maze, cell_size, screen

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

        self.Z = pygame.transform.scale(pygame.image.load('data/mazeparts/Z-переход.png'),
                                        (cell_size, cell_size))
        self.S = pygame.transform.scale(pygame.image.load('data/mazeparts/S-переход.png'),
                                        (cell_size, cell_size))
        self.M = pygame.transform.scale(pygame.image.load('data/mazeparts/M-переход.png'),
                                        (cell_size, cell_size))
        self.W = pygame.transform.scale(pygame.image.load('data/mazeparts/W-переход.png'),
                                        (cell_size, cell_size))

        self.rotate_angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/центр поворот ↑→.png'),
                                                     (cell_size, cell_size))

        self.rotate_angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/центр поворот ↑←.png'),
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
        self.rect.x = self.x
        self.rect.y = self.y

        self.counter = 0
        self.path = iter([])

        self.last_seconds = 0

        self.angry = False  # злой режим для Блинки
        self.dispersion = True  # режим разбегания
        self.in_the_game = False  # призрак в игре/не в игре

    def move(self, end=None):
        global disarming, seconds, level
        coord_y = int((self.y + 11) // cell_size)
        coord_x = int((self.x + 11) // cell_size)
        try:
            if self.counter == 0:
                if end:
                    pre_path = find_path(
                        nodes_matrix[coord_y][coord_x],
                        nodes_matrix[int((end[1] + 11) // cell_size)]
                        [int((end[0] + 11) // cell_size)])
                    if pre_path:
                        self.path = iter(pre_path)
                self.direction = next(self.path)
                self.counter = (8 if self.angry else 16) if not disarming else 24
                self.speed = (3 if self.angry else 1.5) if not disarming else 1
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
            self.rect.x = self.x
            self.rect.y = self.y
            self.counter -= 1
        except StopIteration:
            pass

        if disarming:
            if self.last_seconds == 0:
                self.last_seconds = seconds

            time_shift = round(10 - level // 2 - (seconds - self.last_seconds), 2)

            if time_shift in [10, 2.97, 2.32, 1.65, 0.98, 0.33]:
                self.animation = [load_image('data/ghosts/killing/disarmed1.png'),
                                  load_image('data/ghosts/killing/disarmed2.png')]
            elif time_shift in [3.3, 2.65, 1.98, 1.32, 0.65]:
                self.animation = [load_image('data/ghosts/killing/end-disarmed1.png'),
                                  load_image('data/ghosts/killing/end-disarmed2.png')]
            elif time_shift == 0:
                disarming = False
                self.last_seconds = 0


class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.animation = [load_image('data/ghosts/blinky/right1.png'), load_image('data/ghosts/blinky/right2.png')]

    def move(self, end=None):
        global disarming

        super().move(end)
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


class Pac_man:
    def __init__(self, x, y, direction):
        self.x, self.y = x, y

        self.animation = [load_image('data/pacman/full.png')] * 3
        self.rect = self.animation[0].get_rect()
        self.mask = pygame.mask.from_surface(self.animation[0])
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = 180
        self.direction = direction

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
        self.eaten = False

    def update(self):
        if pygame.sprite.collide_mask(self, pacman) and not self.eaten:
            self.eaten = True
            points_sprite.remove(self)


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

    def update(self):
        global disarming
        if pygame.sprite.collide_mask(self, pacman) and not self.eaten:
            disarming = True
            super().update()


class Fruits(Object):
    def __init__(self, x, y):
        super().__init__(x, y)


if __name__ == '__main__':
    fps = 60
    running = True
    disarming = False
    level, seconds = 1, 0
    points_sprite = pygame.sprite.Group()
    food = []

    for line in nodes_matrix:
        for cell in line:
            if cell.has_food:
                food.append(Point(cell.x * cell_size, cell.y * cell_size))
            elif cell.has_energy:
                food.append(Energizer(cell.x * cell_size, cell.y * cell_size))

    pacman = Pac_man(cell_size * 14 - 11, cell_size * 23 - 11, (0, 0))
    blinky = Blinky(cell_size * 1 - 11, cell_size * 1 - 11)
    points_sprite.draw(screen)

    clock = pygame.time.Clock()
    global_frame, frame = 0, 0
    screen.fill((0, 0, 0))
    ex = Field()
    blinky.move((pacman.x, pacman.y))
    while running:
        ex.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.direction = (-1, 0)
                    pacman.animation = [load_image('data/pacman/left1.png', -1),
                                        load_image('data/pacman/left2.png', -1),
                                        load_image('data/pacman/full.png')]
                elif event.key == pygame.K_RIGHT:
                    pacman.direction = (1, 0)
                    pacman.animation = [load_image('data/pacman/right1.png', -1),
                                        load_image('data/pacman/right2.png', -1),
                                        load_image('data/pacman/full.png')]
                elif event.key == pygame.K_UP:
                    pacman.direction = (0, -1)
                    pacman.animation = [load_image('data/pacman/up1.png', -1),
                                        load_image('data/pacman/up2.png', -1),
                                        load_image('data/pacman/full.png')]
                elif event.key == pygame.K_DOWN:
                    pacman.direction = (0, 1)
                    pacman.animation = [load_image('data/pacman/down1.png', -1),
                                        load_image('data/pacman/down2.png', -1),
                                        load_image('data/pacman/full.png')]
                elif event.key == pygame.K_SPACE:
                    blinky.angry = not blinky.angry

        if global_frame % 4 == 0:
            frame += 1
        points_sprite.draw(screen)
        screen.blit(pacman.animation[frame % 3], (pacman.x, pacman.y))
        screen.blit(blinky.animation[frame % 2], (blinky.x, blinky.y))
        global_frame += 1
        seconds = global_frame / fps

        pacman.move()
        blinky.move((pacman.x, pacman.y))

        for f in food:
            f.update()

        clock.tick(fps)
        pygame.display.flip()
pygame.quit()

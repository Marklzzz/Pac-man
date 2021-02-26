import pygame
import os

from typing import List, Optional, Set, Tuple
from maps import Cell, nodes_matrix


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
    while to_node is not None:
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

import pygame
from typing import List, Optional, Set, Union
from maps import nodes_matrix


class Cell:
    def __init__(self, x, y, cell_type: Union[int, str] = 0, food: int = 1):
        '''cell_type: 0 или field для поля, 1 или wall для стены, по умолчанию 0\n
        food: для еды 1, для энергии 10, по умолчанию 1, если клетка является полем'''
        self.x, self.y = x, y  # Координаты клетки
        self.previous = None  # Предыдущий оптимальный по пути узел графа.
        self.cost = 2  # Цена узла графа. Необходима для расчёта
        if isinstance(cell_type, str):
            self.type = cell_type  # field для ячейки, по которой можно ходить, и wall для ячейки, являющейся стеной.
        else:
            self.type = 'field' if cell_type == 0 else 'wall'

        # Думаю, как реализовать наличие еды в клетке. Для self.type == 'wall' можно определять None.
        self.has_food = (True if food == 1 else False) if self.type != 'wall' else None
        # Думаю, как реализовать наличие энерджайзера в клетке. Для self.type == 'wall' можно определять None.
        self.has_energy = (True if food == 10 else False) if self.type != 'wall' else None

    def reset(self):
        # Сброс характеристик клетки для построения следующего пути.
        self.previous = None
        self.cost = 2

    def __repr__(self) -> str:
        return ('0' if self.x < 10 else '') + str(self.x) + '-' + ('0' if self.y < 10 else '') + str(self.y)

    def __str__(self) -> str:
        return '-' if self.type == 'wall' else ('E' if self.has_energy else ('F' if self.has_food else '0'))


def find_path(start_node: Cell, end_node: Cell) -> Optional[List[Cell]]:
    global nodes_matrix

    start_node.cost = 0

    reachable = [start_node]
    explored = []

    while reachable:
        node = choose_node(reachable, end_node)

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
                (s_x, s_y) == (0, 0) or
                len(nodes_matrix) in [y + s_y, x + s_x] or
                len(nodes_matrix[0]) in [y + s_y, x + s_x] or
                -1 in [y + s_y, x + s_x]
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


def estimate_distance(node: Cell, goal_node: Cell) -> int:
    return abs(node.x - goal_node.x) + abs(node.y - goal_node.y)


def choose_node(reachable: List[Cell], goal_node: Cell) -> Cell:
    min_cost = 58
    best_node = None

    for node in reachable:
        cost_start_to_node = node.cost
        cost_node_to_goal = estimate_distance(node, goal_node)
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
    ['x', *[1 for _ in range(11)]],
    ['x', 1, *[0 for _ in range(9)], 1],
    ['x', 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 'x'],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, *[0 for _ in range(10)]],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1]
]

matrix_full = create_full_matrix(matrix_part)

for i in matrix_full:
    print(i)
pygame.init()

size = 960, 960
screen = pygame.display.set_mode(size)
size_of_parts = 36


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

        self.angle_frame_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока 2↑←.png'),
                                                    (size_of_parts, size_of_parts))
        self.angle_frame_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока 2↑→.png'),
                                                    (size_of_parts, size_of_parts))
        self.angle_frame_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока 2↓←.png'),
                                                    (size_of_parts, size_of_parts))
        self.angle_frame_4 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол блока 2↓→.png'),
                                                    (size_of_parts, size_of_parts))

        self.Z = pygame.transform.scale(pygame.image.load('data/mazeparts/Z-переход.png'),
                                        (size_of_parts, size_of_parts))
        self.S = pygame.transform.scale(pygame.image.load('data/mazeparts/S-переход.png'),
                                        (size_of_parts, size_of_parts))
        self.M = pygame.transform.scale(pygame.image.load('data/mazeparts/M-переход.png'),
                                        (size_of_parts, size_of_parts))
        self.W = pygame.transform.scale(pygame.image.load('data/mazeparts/W-переход.png'),
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

        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass

    def make_first_line(self):
        screen.blit(self.angle_1, (0, 0))
        for i in range(1, 10):
            screen.blit(self.wall_1, (i * size_of_parts, 0))
        screen.blit(self.spicific_angle_1, (size_of_parts * 10, 0))
        screen.blit(self.spicific_angle_2, (size_of_parts * 11, 0))
        for i in range(1, 10):
            screen.blit(self.wall_1, (size_of_parts * 11 + i * size_of_parts, 0))
        screen.blit(self.angle_2, (size_of_parts * 21, 0))

    def make_second_line(self):
        screen.blit(self.wall_2, (0, size_of_parts))
        screen.blit(self.frame_1, (size_of_parts * 10, size_of_parts))
        screen.blit(self.frame_2, (size_of_parts * 11, size_of_parts))
        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts))

    def make_third_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 2))
        screen.blit(self.angle_1, (size_of_parts * 2, size_of_parts * 2))
        screen.blit(self.wall_1, (size_of_parts * 3, size_of_parts * 2))
        screen.blit(self.angle_2, (size_of_parts * 4, size_of_parts * 2))
        screen.blit(self.angle_1, (size_of_parts * 6, size_of_parts * 2))
        screen.blit(self.wall_1, (size_of_parts * 7, size_of_parts * 2))
        screen.blit(self.angle_2, (size_of_parts * 8, size_of_parts * 2))
        screen.blit(self.frame_1, (size_of_parts * 10, size_of_parts * 2))
        screen.blit(self.frame_2, (size_of_parts * 11, size_of_parts * 2))
        screen.blit(self.angle_1, (size_of_parts * 13, size_of_parts * 2))
        screen.blit(self.wall_1, (size_of_parts * 14, size_of_parts * 2))
        screen.blit(self.angle_2, (size_of_parts * 15, size_of_parts * 2))
        screen.blit(self.angle_1, (size_of_parts * 17, size_of_parts * 2))
        screen.blit(self.wall_1, (size_of_parts * 18, size_of_parts * 2))
        screen.blit(self.angle_2, (size_of_parts * 19, size_of_parts * 2))
        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts * 2))

    def make_fourth_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 3))
        screen.blit(self.wall_2, (size_of_parts * 2, size_of_parts * 3))
        screen.blit(self.wall_3, (size_of_parts * 4, size_of_parts * 3))
        screen.blit(self.wall_2, (size_of_parts * 6, size_of_parts * 3))
        screen.blit(self.wall_3, (size_of_parts * 8, size_of_parts * 3))
        screen.blit(self.frame_1, (size_of_parts * 10, size_of_parts * 3))
        screen.blit(self.frame_2, (size_of_parts * 11, size_of_parts * 3))
        screen.blit(self.wall_2, (size_of_parts * 13, size_of_parts * 3))
        screen.blit(self.wall_3, (size_of_parts * 15, size_of_parts * 3))
        screen.blit(self.wall_2, (size_of_parts * 17, size_of_parts * 3))
        screen.blit(self.wall_3, (size_of_parts * 19, size_of_parts * 3))
        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts * 3))

    def make_fifth_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 4))
        screen.blit(self.angle_3, (size_of_parts * 2, size_of_parts * 4))
        screen.blit(self.wall_4, (size_of_parts * 3, size_of_parts * 4))
        screen.blit(self.angle_4, (size_of_parts * 4, size_of_parts * 4))
        screen.blit(self.angle_3, (size_of_parts * 6, size_of_parts * 4))
        screen.blit(self.wall_4, (size_of_parts * 7, size_of_parts * 4))
        screen.blit(self.angle_4, (size_of_parts * 8, size_of_parts * 4))
        screen.blit(self.angle_frame_3, (size_of_parts * 10, size_of_parts * 4))
        screen.blit(self.angle_frame_4, (size_of_parts * 11, size_of_parts * 4))
        screen.blit(self.angle_3, (size_of_parts * 13, size_of_parts * 4))
        screen.blit(self.wall_4, (size_of_parts * 14, size_of_parts * 4))
        screen.blit(self.angle_4, (size_of_parts * 15, size_of_parts * 4))
        screen.blit(self.angle_3, (size_of_parts * 17, size_of_parts * 4))
        screen.blit(self.wall_4, (size_of_parts * 18, size_of_parts * 4))
        screen.blit(self.angle_4, (size_of_parts * 19, size_of_parts * 4))
        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts * 4))

    def make_sixth_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 5))
        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts * 5))

    def make_seventh_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 6))

        screen.blit(self.angle_1, (size_of_parts * 2, size_of_parts * 6))
        screen.blit(self.wall_1, (size_of_parts * 3, size_of_parts * 6))
        screen.blit(self.angle_2, (size_of_parts * 4, size_of_parts * 6))

        screen.blit(self.angle_1, (size_of_parts * 6, size_of_parts * 6))
        screen.blit(self.angle_2, (size_of_parts * 7, size_of_parts * 6))

        screen.blit(self.angle_1, (size_of_parts * 9, size_of_parts * 6))
        screen.blit(self.wall_1, (size_of_parts * 10, size_of_parts * 6))
        screen.blit(self.wall_1, (size_of_parts * 11, size_of_parts * 6))
        screen.blit(self.angle_2, (size_of_parts * 12, size_of_parts * 6))

        screen.blit(self.angle_1, (size_of_parts * 14, size_of_parts * 6))
        screen.blit(self.angle_2, (size_of_parts * 15, size_of_parts * 6))

        screen.blit(self.angle_1, (size_of_parts * 17, size_of_parts * 6))
        screen.blit(self.wall_1, (size_of_parts * 18, size_of_parts * 6))
        screen.blit(self.angle_2, (size_of_parts * 19, size_of_parts * 6))

        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts * 6))

    def make_eight_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 7))

        screen.blit(self.angle_3, (size_of_parts * 2, size_of_parts * 7))
        screen.blit(self.wall_4, (size_of_parts * 3, size_of_parts * 7))
        screen.blit(self.angle_4, (size_of_parts * 4, size_of_parts * 7))

        screen.blit(self.wall_2, (size_of_parts * 6, size_of_parts * 7))
        screen.blit(self.wall_3, (size_of_parts * 7, size_of_parts * 7))

        screen.blit(self.angle_3, (size_of_parts * 9, size_of_parts * 7))
        screen.blit(self.frame_3, (size_of_parts * 10, size_of_parts * 7))
        screen.blit(self.frame_3, (size_of_parts * 11, size_of_parts * 7))
        screen.blit(self.angle_4, (size_of_parts * 12, size_of_parts * 7))

        screen.blit(self.wall_2, (size_of_parts * 14, size_of_parts * 7))
        screen.blit(self.wall_3, (size_of_parts * 15, size_of_parts * 7))

        screen.blit(self.angle_3, (size_of_parts * 17, size_of_parts * 7))
        screen.blit(self.wall_4, (size_of_parts * 18, size_of_parts * 7))
        screen.blit(self.angle_4, (size_of_parts * 19, size_of_parts * 7))

        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts * 7))

    def make_nine_line(self):
        screen.blit(self.wall_2, (0, size_of_parts * 8))
        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts * 8))

        screen.blit(self.wall_2, (size_of_parts * 6, size_of_parts * 8))
        screen.blit(self.wall_3, (size_of_parts * 7, size_of_parts * 8))

        screen.blit(self.angle_frame_2, (size_of_parts * 10, size_of_parts * 8))
        screen.blit(self.angle_frame_1, (size_of_parts * 11, size_of_parts * 8))

        screen.blit(self.wall_2, (size_of_parts * 14, size_of_parts * 8))
        screen.blit(self.wall_3, (size_of_parts * 15, size_of_parts * 8))

        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts * 8))

    def make_tenth_line(self):
        screen.blit(self.angle_3, (0, size_of_parts * 9))

        for i in range(1, 4):
            screen.blit(self.wall_4, (size_of_parts * i, size_of_parts * 9))

        screen.blit(self.angle_2, (size_of_parts * 4, size_of_parts * 9))

        screen.blit(self.wall_2, (size_of_parts * 6, size_of_parts * 9))
        screen.blit(self.frame_1, (size_of_parts * 7, size_of_parts * 9))
        screen.blit(self.M, (size_of_parts * 8, size_of_parts * 9))

        screen.blit(pygame.transform.rotate(self.angle_frame_2, 180), (size_of_parts * 10, size_of_parts * 9))
        screen.blit(pygame.transform.rotate(self.angle_frame_1, 180), (size_of_parts * 11, size_of_parts * 9))

        screen.blit(self.W, (size_of_parts * 13, size_of_parts * 9))
        screen.blit(self.frame_2, (size_of_parts * 14, size_of_parts * 9))
        screen.blit(self.wall_3, (size_of_parts * 15, size_of_parts * 9))

        screen.blit(self.angle_1, (size_of_parts * 17, size_of_parts * 9))

        for i in range(1, 4):
            screen.blit(self.wall_4, (size_of_parts * (17 + i), size_of_parts * 9))

        screen.blit(self.angle_4, (size_of_parts * 21, size_of_parts * 9))

    def make_eleventh_line(self):
        pass


ex = Field()

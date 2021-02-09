from typing import List, Union


class Cell:
    def __init__(self, x, y, cell_type: Union[int, str] = 0, food: int = 1):
        '''cell_type: 0 или field для поля, 1 или wall для стены, по умолчанию 0\n
        food: для еды 1, для энергии 10, по умолчанию 1, если клетка является полем'''
        self.x, self.y = x, y  # Координаты клетки
        self.previous = None  # Предыдущий оптимальный по пути узел графа.
        self.cost = 58  # Цена узла графа. Необходима для расчёта
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
        self.cost = 58

    def __repr__(self) -> str:
        return ('0' if self.x < 10 else '') + str(self.x) + '-' + ('0' if self.y < 10 else '') + str(self.y)

    def __str__(self) -> str:
        return '-' if self.type == 'wall' else ('E' if self.has_energy else ('F' if self.has_food else '0'))


r = range
nodes_matrix: List[List[Cell]] = [
    # ----------------------------
    [Cell(x, 0, 1) for x in r(28)],
    # -FFFFFFFFFFFF--FFFFFFFFFFFF-
    [Cell(0, 1, 1), *(Cell(x, 1) for x in r(1, 13)), Cell(13, 1, 1),
     Cell(14, 1, 1), *(Cell(x, 1) for x in r(15, 27)), Cell(27, 1, 1)],
    # -F----F-----F--F-----F----F-
    [Cell(0, 2, 1), Cell(1, 2), *(Cell(x, 2, 1) for x in r(2, 6)), Cell(6, 2), *(Cell(x, 2, 1) for x in r(7, 12)),
     Cell(12, 2), Cell(13, 2, 1), Cell(14, 2, 1), Cell(15, 2), *(Cell(x, 2, 1) for x in r(16, 21)), Cell(21, 2),
     *(Cell(x, 2, 1) for x in r(22, 26)), Cell(26, 2), Cell(27, 2, 1)],
    # -E----F-----F--F-----F----E-
    [Cell(0, 3, 1), Cell(1, 3, 0, 10), *(Cell(x, 3, 1) for x in r(2, 6)), Cell(6, 3), *(Cell(x, 3, 1) for x in r(7, 12)),
     Cell(12, 3), Cell(13, 3, 1), Cell(14, 3, 1), Cell(15, 3), *(Cell(x, 3, 1) for x in r(16, 21)), Cell(21, 3),
     *(Cell(x, 3, 1) for x in r(22, 26)), Cell(26, 3, 0, 10), Cell(27, 3, 1)],
    # -F----F-----F--F-----F----F-
    [Cell(0, 4, 1), Cell(1, 4), *(Cell(x, 4, 1) for x in r(2, 6)), Cell(6, 4), *(Cell(x, 4, 1) for x in r(7, 12)),
     Cell(12, 4), Cell(13, 4, 1), Cell(14, 4, 1), Cell(15, 4), *(Cell(x, 4, 1) for x in r(16, 21)), Cell(21, 4),
     *(Cell(x, 4, 1) for x in r(22, 26)), Cell(26, 4), Cell(27, 4, 1)],
    # -FFFFFFFFFFFFFFFFFFFFFFFFFF-
    [Cell(0, 5, 1), *(Cell(x, 5) for x in r(1, 27)), Cell(27, 5, 1)],
    # -F----F--F--------F--F----F-
    [Cell(0, 6, 1), Cell(1, 6), *(Cell(x, 6, 1) for x in r(2, 6)), Cell(6, 6), Cell(7, 6, 1), Cell(8, 6, 1),
     Cell(9, 6), *(Cell(x, 6, 1) for x in r(10, 18)), Cell(18, 6), Cell(19, 6, 1), Cell(20, 6, 1), Cell(21, 6),
     *(Cell(x, 6, 1) for x in r(22, 26)), Cell(26, 6), Cell(27, 6, 1)],
    # -F----F--F--------F--F----F-
    [Cell(0, 7, 1), Cell(1, 7), *(Cell(x, 7, 1) for x in r(2, 6)), Cell(6, 7), Cell(7, 7, 1), Cell(8, 7, 1),
     Cell(9, 7), *(Cell(x, 7, 1) for x in r(10, 18)), Cell(18, 7), Cell(19, 7, 1), Cell(20, 7, 1), Cell(21, 7),
     *(Cell(x, 7, 1) for x in r(22, 26)), Cell(26, 7), Cell(27, 7, 1)],
    # -FFFFFF--FFFF--FFFF--FFFFFF-
    [Cell(0, 8, 1), *(Cell(x, 8) for x in r(1, 7)), Cell(7, 8, 1), Cell(8, 8, 1), *(Cell(x, 8) for x in r(9, 13)),
     Cell(13, 8, 1), Cell(14, 8, 1), *(Cell(x, 8) for x in r(15, 19)), Cell(19, 8, 1), Cell(20, 8, 1),
     *(Cell(x, 8) for x in r(21, 27)), Cell(27, 8, 1)],
    # ------F----- -- -----F------
    [*(Cell(x, 9, 1) for x in r(0, 6)), Cell(6, 9), *(Cell(x, 9, 1) for x in r(7, 12)), Cell(12, 9, 0, 0),
     Cell(13, 9, 1), Cell(14, 9, 1), Cell(15, 9, 0, 0), *(Cell(x, 9, 1) for x in r(16, 21)),
     Cell(21, 9), *(Cell(x, 9, 1) for x in r(22, 28))],
    # ------F----- -- -----F------
    [*(Cell(x, 10, 1) for x in r(0, 6)), Cell(6, 10), *(Cell(x, 10, 1) for x in r(7, 12)), Cell(12, 10, 0, 0),
     Cell(13, 10, 1), Cell(14, 10, 1), Cell(15, 10, 0, 0), *(Cell(x, 10, 1) for x in r(16, 21)), Cell(21, 10),
     *(Cell(x, 10, 1) for x in r(22, 28))],
    # ------F--          --F------
    [*(Cell(x, 11, 1) for x in r(0, 6)), Cell(6, 11), Cell(7, 11, 1), Cell(8, 11, 1),
     *(Cell(x, 11, 0, 0) for x in r(9, 19)), Cell(19, 11, 1), Cell(20, 11, 1), Cell(21, 11),
     *(Cell(x, 11, 1) for x in r(22, 28))],
    # ------F-- ---  --- --F------
    [*(Cell(x, 12, 1) for x in r(0, 6)), Cell(6, 12), Cell(7, 12, 1), Cell(8, 12, 1), Cell(9, 12, 0, 0),
     *(Cell(x, 12, 1) for x in r(10, 13)), Cell(13, 12, 0, 0), Cell(14, 12, 0, 0), *(Cell(x, 12, 1) for x in r(15, 18)),
     Cell(18, 12, 0, 0), Cell(19, 12, 1), Cell(20, 12, 1), Cell(21, 12), *(Cell(x, 12, 1) for x in r(22, 28))],
    # ------F-- -      - --F------
    [*(Cell(x, 13, 1) for x in r(0, 6)), Cell(6, 13), Cell(7, 13, 1), Cell(8, 13, 1), Cell(9, 13, 0, 0), Cell(10, 13, 1),
     *(Cell(x, 13, 0, 0) for x in r(11, 17)), Cell(17, 13, 1), Cell(18, 13, 0, 0), Cell(19, 13, 1), Cell(20, 13, 1),
     Cell(21, 13), *(Cell(x, 13, 1) for x in r(22, 28))],
    #       F   -      -   F
    [*(Cell(x, 14, 0, 0) for x in r(0, 6)), Cell(6, 14), *(Cell(x, 14, 0, 0) for x in r(7, 10)), Cell(10, 14, 1),
     *(Cell(x, 14, 0, 0) for x in r(11, 17)), Cell(17, 14, 1), *(Cell(x, 14, 0, 0) for x in r(18, 21)), Cell(21, 14),
     *(Cell(x, 14, 0, 0) for x in r(22, 28)), Cell(28, 14, 0, 0)],
    # ------F-- -      - --F------
    [*(Cell(x, 15, 1) for x in r(0, 6)), Cell(6, 15), Cell(7, 15, 1), Cell(8, 15, 1), Cell(9, 15, 0, 0), Cell(10, 15, 1),
     *(Cell(x, 15, 0, 0) for x in r(11, 17)), Cell(17, 15, 1), Cell(18, 15, 0, 0), Cell(19, 15, 1), Cell(20, 15, 1),
     Cell(21, 15), *(Cell(x, 15, 1) for x in r(22, 28))],
    # ------F-- -------- --F------
    [*(Cell(x, 16, 1) for x in r(0, 6)), Cell(6, 16), Cell(7, 16, 1), Cell(8, 16, 1), Cell(9, 16, 0, 0),
     *(Cell(x, 16, 1) for x in r(10, 18)), Cell(18, 16, 0, 0), Cell(19, 16, 1), Cell(20, 16, 1), Cell(21, 16),
     *(Cell(x, 16, 1) for x in r(22, 28))],
    # ------F--          --F------
    [*(Cell(x, 17, 1) for x in r(0, 6)), Cell(6, 17), Cell(7, 17, 1), Cell(8, 17, 1),
     *(Cell(x, 17, 0, 0) for x in r(9, 19)), Cell(19, 17, 1), Cell(20, 17, 1), Cell(21, 17),
     *(Cell(x, 17, 1) for x in r(22, 28))],
    # ------F-- -------- --F----F-
    [*(Cell(x, 18, 1) for x in r(0, 6)), Cell(6, 18), Cell(7, 18, 1), Cell(8, 18, 1), Cell(9, 18, 0, 0),
     *(Cell(x, 18, 1) for x in r(10, 18)), Cell(18, 18, 0, 0), Cell(19, 18, 1), Cell(20, 18, 1), Cell(21, 18),
     *(Cell(x, 18, 1) for x in r(22, 28))],
    # ------F-- -------- --F----F-
    [*(Cell(x, 19, 1) for x in r(0, 6)), Cell(6, 19), Cell(7, 19, 1), Cell(8, 19, 1), Cell(9, 19, 0, 0),
     *(Cell(x, 19, 1) for x in r(10, 18)), Cell(18, 19, 0, 0), Cell(19, 19, 1), Cell(20, 19, 1), Cell(21, 19),
     *(Cell(x, 19, 1) for x in r(22, 28))],
    # -FFFFFFFFFFFF--FFFFFFFFFFFF-
    [Cell(0, 20, 1), *(Cell(x, 20) for x in r(1, 13)), Cell(13, 20, 1),
     Cell(14, 20, 1), *(Cell(x, 20) for x in r(15, 27)), Cell(27, 20, 1)],
    # -F----F-----F--F-----F----F-
    [Cell(0, 21, 1), Cell(1, 21), *(Cell(x, 21, 1) for x in r(2, 6)), Cell(6, 21), *(Cell(x, 21, 1) for x in r(7, 12)),
     Cell(12, 21), Cell(13, 21, 1), Cell(14, 21, 1), Cell(15, 21), *(Cell(x, 21, 1) for x in r(16, 21)), Cell(21, 21),
     *(Cell(x, 21, 1) for x in r(22, 26)), Cell(26, 21), Cell(27, 21, 1)],
    # -F----F-----F--F-----F----F-
    [Cell(0, 22, 1), Cell(1, 22), *(Cell(x, 22, 1) for x in r(2, 6)), Cell(6, 22), *(Cell(x, 22, 1) for x in r(7, 12)),
     Cell(12, 22), Cell(13, 22, 1), Cell(14, 22, 1), Cell(15, 22), *(Cell(x, 22, 1) for x in r(16, 21)),
     Cell(21, 22), *(Cell(x, 22, 1) for x in r(22, 26)), Cell(26, 22), Cell(27, 22, 1)],
    # -EFF--FFFFFFF00FFFFFFF--FFE-
    [Cell(0, 23, 1), Cell(1, 23, 0, 10), Cell(2, 23), Cell(3, 23), Cell(4, 23, 1), Cell(5, 23, 1),
     *(Cell(x, 23) for x in r(6, 13)), Cell(13, 23, 0, 0), Cell(14, 23, 0, 0), *(Cell(x, 23) for x in r(15, 22)),
     Cell(22, 23, 1), Cell(23, 23, 1), Cell(24, 23), Cell(25, 23), Cell(26, 23, 0, 10), Cell(27, 23, 1)],
    # ---F--F--F--------F--F--F---
    [*(Cell(x, 24, 1) for x in r(0, 3)), Cell(3, 24), Cell(4, 24, 1), Cell(5, 24, 1), Cell(6, 24), Cell(7, 24, 1),
     Cell(8, 24, 1), Cell(9, 24), *(Cell(x, 24, 1) for x in r(10, 18)), Cell(18, 24), Cell(19, 24, 1), Cell(20, 24, 1),
     Cell(21, 24), Cell(22, 24, 1), Cell(23, 24, 1), Cell(24, 24), *(Cell(x, 24, 1) for x in r(25, 28))],
    # ---F--F--F--------F--F--F---
    [*(Cell(x, 25, 1) for x in r(0, 3)), Cell(3, 25), Cell(4, 25, 1), Cell(5, 25, 1), Cell(6, 25), Cell(7, 25, 1),
     Cell(8, 25, 1), Cell(9, 25), *(Cell(x, 25, 1) for x in r(10, 18)), Cell(18, 25), Cell(19, 25, 1), Cell(20, 25, 1),
     Cell(21, 25), Cell(22, 25, 1), Cell(23, 25, 1), Cell(24, 25), *(Cell(x, 25, 1) for x in r(25, 28))],
    # -FFFFFF--FFFF--FFFF--FFFFFF-
    [Cell(0, 26, 1), *(Cell(x, 26) for x in r(1, 7)), Cell(7, 26, 1), Cell(8, 26, 1), *(Cell(x, 26) for x in r(9, 13)),
     Cell(13, 26, 1), Cell(14, 26, 1), *(Cell(x, 26) for x in r(15, 19)), Cell(19, 26, 1), Cell(20, 26, 1),
     *(Cell(x, 26) for x in r(21, 27)), Cell(27, 26, 1)],
    # -F----------F--F----------F-
    [Cell(0, 27, 1), Cell(1, 27), *(Cell(x, 27, 1) for x in r(2, 12)), Cell(12, 27), Cell(13, 27, 1),
     Cell(14, 27, 1), Cell(15, 27), *(Cell(x, 27, 1) for x in r(16, 26)), Cell(26, 27), Cell(27, 27, 1)],
    # -F----------F--F----------F-
    [Cell(0, 28, 1), Cell(1, 28), *(Cell(x, 28, 1) for x in r(2, 12)), Cell(12, 28), Cell(13, 28, 1),
     Cell(14, 28, 1), Cell(15, 28), *(Cell(x, 28, 1) for x in r(16, 26)), Cell(26, 28), Cell(27, 28, 1)],
    # -FFFFFFFFFFFFFFFFFFFFFFFFFF-
    [Cell(0, 29, 1), *(Cell(x, 29) for x in r(1, 27)), Cell(27, 29, 1)],
    # ----------------------------
    [Cell(x, 30, 1) for x in r(28)]
]


if __name__ == '__main__':
    print(*[''.join([str(el) for el in l])for l in nodes_matrix], sep='\n')

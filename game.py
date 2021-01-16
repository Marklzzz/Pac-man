import pygame


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

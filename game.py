import pygame


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

        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass

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



ex = Field()

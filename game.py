import pygame




def create_full_matrix(matrix):
    for i in range(len(matrix)):
        matrix[i] = [*matrix[i], *matrix[i][::-1]]
    return matrix


matrix_part = [
    [1 for _ in range(11)],
    [1, *[0 for _ in range(9)], 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
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





class Field:
    def __init__(self):
        size = 960, 960
        size_of_parts = 32
        screen = pygame.display.set_mode(size)

        self.wall_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты ↑.png'),
                                             (size_of_parts, size_of_parts))
        self.wall_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты ←.png'),
                                             (size_of_parts, size_of_parts))
        self.wall_3 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт карты →.png'),
                                             (size_of_parts, size_of_parts))

        self.spicific_angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑→.png'),
                                                       (size_of_parts, size_of_parts))
        self.spicific_angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑←.png'),
                                                       (size_of_parts, size_of_parts))

        self.angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↑←.png'),
                                              (size_of_parts, size_of_parts))
        self.angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↑→.png'),
                                              (size_of_parts, size_of_parts))
        screen.blit(self.angle_1, (0, 0))

        for i in range(1, 10):
            screen.blit(self.wall_1, (i * size_of_parts, 0))

        screen.blit(self.spicific_angle_1, (size_of_parts * 10, 0))

        screen.blit(self.spicific_angle_2, (size_of_parts * 11, 0))

        for i in range(1, 10):
            screen.blit(self.wall_1, (size_of_parts * 11 + i * size_of_parts, 0))


        screen.blit(self.angle_2, (size_of_parts * 21, 0))


        screen.blit(self.wall_2, (0, size_of_parts))

        self.frame_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока →.png'),
                                              (size_of_parts, size_of_parts))

        self.frame_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/борт блока ←.png'),
                                              (size_of_parts, size_of_parts))

        screen.blit(self.frame_1, (size_of_parts * 10, size_of_parts))
        screen.blit(self.frame_2, (size_of_parts * 11, size_of_parts))
        screen.blit(self.wall_3, (size_of_parts * 21, size_of_parts))



        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass
        pygame.quit()


ex = Field()

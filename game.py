import pygame

pygame.init()

class Field:
    def __init__(self):
        size = 720, 720
        size_of_parts = 24
        screen = pygame.display.set_mode(size)
        self.angle_1 = pygame.image.load('data/mazeparts/угол карты ↑←.png')
        self.angle_1 = pygame.transform.scale(self.angle_1, (size_of_parts, size_of_parts))
        screen.blit(self.angle_1, (0, 0))

        for i in range(1, 10):
            wall = pygame.image.load('data/mazeparts/борт карты ↑.png')
            wall = pygame.transform.scale(wall, (size_of_parts, size_of_parts))
            screen.blit(wall, (i * size_of_parts, 0))

        self.spicific_angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑→.png'), (size_of_parts, size_of_parts))
        screen.blit(self.spicific_angle_1, (size_of_parts * 10, 0))

        self.spicific_angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑←.png'), (size_of_parts, size_of_parts))
        screen.blit(self.spicific_angle_2, (size_of_parts * 11, 0))

        for i in range(1, 10):
            wall = pygame.image.load('data/mazeparts/борт карты ↑.png')
            wall = pygame.transform.scale(wall, (size_of_parts, size_of_parts))
            screen.blit(wall, (size_of_parts * 11 + i * size_of_parts, 0))

        self.angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↑→.png'), (size_of_parts, size_of_parts))
        screen.blit(self.angle_2, (size_of_parts * 21, 0))
        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass
        pygame.quit()

ex = Field()
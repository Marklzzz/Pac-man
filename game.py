import pygame

pygame.init()

class Field:
    def __init__(self):
        size = 720, 720
        screen = pygame.display.set_mode(size)
        self.angle_1 = pygame.image.load('data/mazeparts/угол карты ↑←.png')
        self.angle_1 = pygame.transform.scale(self.angle_1, (24, 24))
        screen.blit(self.angle_1, (0, 0))

        for i in range(1, 10):
            wall = pygame.image.load('data/mazeparts/борт карты ↑.png')
            wall = pygame.transform.scale(wall, (24, 24))
            screen.blit(wall, (i * 24, 0))

        self.spicific_angle_1 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑→.png'), (24, 24))
        screen.blit(self.spicific_angle_1, (240, 0))

        self.spicific_angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/поворот внутри карты ↑←.png'), (24, 24))
        screen.blit(self.spicific_angle_2, (264, 0))

        for i in range(1, 10):
            wall = pygame.image.load('data/mazeparts/борт карты ↑.png')
            wall = pygame.transform.scale(wall, (24, 24))
            screen.blit(wall, (264 + i * 24, 0))

        self.angle_2 = pygame.transform.scale(pygame.image.load('data/mazeparts/угол карты ↑→.png'), (24, 24))
        screen.blit(self.angle_2, (504, 0))
        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass
        pygame.quit()

ex = Field()
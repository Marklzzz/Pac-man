import pygame
import os


pygame.init()
width, height = 1000, 1000
size = int(width), int(height)
screen = pygame.display.set_mode(size)


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Pac_man:
    def __init__(self, x, y, direction):
        self.x, self.y = x, y

        self.animation = [load_image('data/pacman/left1.png', -1), load_image('data/pacman/left1.png', -1)]
        self.rect = self.animation[0].get_rect()
        self.mask = pygame.mask.from_surface(self.animation[0])
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = 180
        self.direction = direction
        self.frame = 0

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

    def update(self):
        if pygame.sprite.collide_mask(self, pacman):
            self.kill()


class Point(Object, pygame.sprite.Sprite):
    image = load_image('data/other/s_food.png', -1)

    def __init__(self, x, y):
        super().__init__(x, y, points_sprite)
        self.image = Point.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Energizer(Object, pygame.sprite.Sprite):
    image = load_image('data/other/b_food.png', -1)

    def __init__(self, x, y):
        super().__init__(x, y, points_sprite)
        self.image = Energizer.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Fruits(Object):
    def __init__(self, x, y):
        super().__init__(x, y)


if __name__ == '__main__':
    fps = 60
    running = True
    point = load_image('data/other/s_food.png', -1)
    points_sprite = pygame.sprite.Group()

    pacman = Pac_man(250, 250, (0, 0))

    points = []  # Добавил для наглядности работы поедания поинтов
    x = 10
    y = 270
    for _ in range(10):
        points.append(Point(x, y))
        x += 20

    clock = pygame.time.Clock()
    frame = 0  # Кадр анимациии пакмана
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:  # Управление
                if event.key == pygame.K_LEFT:
                    pacman.direction = (-1, 0)
                    pacman.animation = [load_image('data/pacman/left1.png', -1),
                                        load_image('data/pacman/left2.png', -1)]
                elif event.key == pygame.K_RIGHT:
                    pacman.direction = (1, 0)
                    pacman.animation = [load_image('data/pacman/right1.png', -1),
                                        load_image('data/pacman/right2.png', -1)]
                elif event.key == pygame.K_UP:
                    pacman.direction = (0, -1)
                    pacman.animation = [load_image('data/pacman/up1.png', -1),
                                        load_image('data/pacman/up2.png', -1)]
                elif event.key == pygame.K_DOWN:
                    pacman.direction = (0, 1)
                    pacman.animation = [load_image('data/pacman/down1.png', -1),
                                        load_image('data/pacman/down2.png', -1)]

        if pacman.frame % 15 == 0:  # частота смены анимации
            frame += 1
        for i in points:  # Проверка на столкновение каждого спрайта
            i.update()
        points_sprite.draw(screen)
        screen.blit(pacman.animation[frame % 2], (pacman.x, pacman.y))
        pacman.frame += 1
        pacman.move()

        clock.tick(fps)
        pygame.display.flip()
pygame.quit()

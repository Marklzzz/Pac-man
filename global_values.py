cell_size = 24
size = (28 * cell_size, 36 * cell_size)

important_points = ((6, 1), (21, 1), (1, 5), (6, 5), (9, 5), (12, 5), (15, 5), (18, 5), (21, 5), (26, 5),
                    (6, 8), (21, 8), (12, 11), (15, 11), (6, 14), (9, 14), (18, 14), (21, 14), (9, 17),
                    (18, 17), (6, 20), (9, 20), (18, 20), (21, 20), (6, 23), (9, 23), (12, 23), (15, 23),
                    (18, 23), (21, 23), (3, 26), (24, 26), (12, 26), (15, 26), (26, 1))

fruits_order = [
    (), ('cherry',), ('cherry', 'strawberry'), ('cherry', 'strawberry', 'peach'),
    ('cherry', 'strawberry', 'peach', 'peach'), ('cherry', 'strawberry', 'peach', 'peach', 'apple'),
    ('cherry', 'strawberry', 'peach', 'peach', 'apple', 'apple'),
    ('cherry', 'strawberry', 'peach', 'peach', 'apple', 'apple', 'melon'),
    ('strawberry', 'peach', 'peach', 'apple', 'apple', 'melon', 'melon'),
    ('peach', 'peach', 'apple', 'apple', 'melon', 'melon', 'spaceship'),
    ('peach', 'apple', 'apple', 'melon', 'melon', 'spaceship', 'spaceship'),
    ('apple', 'apple', 'melon', 'melon', 'spaceship', 'spaceship', 'bell'),
    ('apple', 'melon', 'melon', 'spaceship', 'spaceship', 'bell', 'bell'),
    ('melon', 'melon', 'spaceship', 'spaceship', 'bell', 'bell', 'key'),
    ('melon', 'spaceship', 'spaceship', 'bell', 'bell', 'key', 'key'),
    ('spaceship', 'spaceship', 'bell', 'bell', 'key', 'key', 'key'),
    ('spaceship', 'bell', 'bell', 'key', 'key', 'key', 'key'),
    ('bell', 'bell', 'key', 'key', 'key', 'key', 'key'),
    ('bell', 'key', 'key', 'key', 'key', 'key', 'key'),
    ('key', 'key', 'key', 'key', 'key', 'key', 'key'),
]


pacman, points_sprite, level, blinky, seconds, disarming, food, global_frame = 0, 0, 0, 0, 0, 0, 0, 0

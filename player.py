import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.Surface((64, 64)).convert_alpha()
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)
        self.speed = 10
        self.pos = pos
        self.direction = pg.math.Vector2()

    def keylog(self):
        keys = pg.key.get_pressed()

        # movement over the y direction
        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # movement over the x direction
        if keys[pg.K_LEFT]:
            self.direction.x = -1
        elif keys[pg.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def update(self):
        self.keylog()
        self.move()

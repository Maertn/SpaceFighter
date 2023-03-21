import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.Surface((64, 64)).convert_alpha()
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)

        # movement
        self.normal_speed = 4
        self.speed = self.normal_speed
        self.pos = pos
        self.direction = pg.math.Vector2()

        self.dodging = False
        self.dodge_time = None
        self.dodge_cooldown = 300
        self.dodge_speed = 6

    def keylog(self):
        keys = pg.key.get_pressed()
        if not self.dodging:    
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

            # dodge roll
            if keys[pg.K_LCTRL]:
                self.dodging = True
                self.dodge_time = pg.time.get_ticks()
                self.dodgeroll()

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def dodgeroll(self):
        dodge_direction = self.get_direction()
        if self.dodging == True:
            self.speed = self.dodge_speed
            self.direction = dodge_direction
            self.move()
        else:
            self.speed = self.normal_speed
            self.direction = pg.math.Vector2()

    def cooldowns(self):
        current_time = pg.time.get_ticks()
        if self.dodging:
            if current_time - self.dodge_time >= self.dodge_cooldown:
                self.dodging = False

    def get_direction(self):
        current_direction = self.direction
        return current_direction

    def update(self):
        self.keylog()
        self.move()
        self.dodgeroll()
        self.cooldowns()
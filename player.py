import pygame as pg

from bullets import Bullet
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.Surface((32, 32)).convert_alpha()
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)

        # get display surface
        self.display_surface = pg.display.get_surface() 

        # movement
        self.normal_speed = 4
        self.speed = self.normal_speed
        self.pos = pos
        self.direction = pg.math.Vector2()

        # dodging
        self.dodging = False
        self.dodge_time = None
        self.dodge_cooldown = 300
        self.dodge_speed = 6

        # shooting
        self.shooting = False
        self.fire_pattern = 0
        self.wave_pattern = False

        # sprite group for bullets
        self.visible_sprites = pg.sprite.Group()

        # data for level
        self.alive = False
        self.current_score = 0

    def keylog(self):
        keys = pg.key.get_pressed()
        if not self.dodging:    
            # movement over the y direction
            if keys[pg.K_UP] and self.rect.top >= 0:
                self.direction.y = -1
            elif keys[pg.K_DOWN] and self.rect.bottom <= SCREEN_HEIGHT:
                self.direction.y = 1
            else:
                self.direction.y = 0

            # movement over the x direction
            if keys[pg.K_LEFT] and self.rect.left >= GAME_SCREEN_LEFT:
                self.direction.x = -1
            elif keys[pg.K_RIGHT] and self.rect.right <= GAME_SCREEN_RIGHT:
                self.direction.x = 1
            else:
                self.direction.x = 0

            # dodge roll
            if keys[pg.K_LCTRL]:
                self.dodging = True
                self.dodge_time = pg.time.get_ticks()
                self.dodgeroll()
            
            if keys[pg.K_SPACE]:
                self.shooting = True
            else:
                self.shooting = False

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
        """This mehod is used in dodge roll to lock the direction of movement for the player."""
        current_direction = self.direction
        return current_direction

    def update(self):
        self.keylog()
        self.move()
        self.dodgeroll()
        self.cooldowns()
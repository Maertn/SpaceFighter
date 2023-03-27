import pygame as pg
from settings import *

class PowerUp(pg.sprite.Sprite):
    def __init__(self, pos, groups, upgrade, color):
        super().__init__(groups)
        self.image = pg.Surface((12, 12)).convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect(center = pos)
        self.upgrade = upgrade

    def destroy(self):
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()

    def move(self):
        self.rect.centery += 5

    def update(self):
        self.move()
        self.destroy()


# class ShotPower(PowerUp):
#     def __init__(self, pos, groups):
#         super().__init__(groups)

#         self.upgrade = 'fire_pattern'


# class WaveyPower(PowerUp):
#     def __init__(self, pos, groups):
#         super().__init__(groups)

#         self.upgrade = 'wavey_pattern'
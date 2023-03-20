import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.Surface((64, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)
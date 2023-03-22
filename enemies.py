import pygame as pg

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.Surface((32,32)).convert_alpha()
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)

    def destroy_enemy(self):
        if self.rect.centerx <= -50 or self.rect.centerx >= 1300:
            self.kill()

    def update(self):
        self.destroy_enemy()       
        

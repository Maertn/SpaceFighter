import pygame as pg

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.Surface((5, 5)).convert_alpha()
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.pos = pos

    def trajectory(self):
        self.rect.centery -= 20
        
    def remove_bullet(self):
        if self.rect.centery <= 0:
            self.kill()

    def update(self):
        self.trajectory()
        self.remove_bullet()
        print('shooting')

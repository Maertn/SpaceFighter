import pygame as pg

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.Surface((5, 5)).convert_alpha()
        self.color = 'white'
        self.rect = self.image.get_rect(center = pos)   
        self.direction = -20

    def trajectory(self):
        self.rect.centery += self.direction
        
    def remove_bullet(self):
        if self.rect.centery <= 0 or self.rect.centery >= 720:
            self.kill()

    def color_bullet(self):
        self.image.fill(self.color)

    def update(self):
        self.trajectory()
        self.remove_bullet()
        self.color_bullet()


class EnemyBullet(Bullet):
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        self.direction = 20
        self.color = 'yellow'
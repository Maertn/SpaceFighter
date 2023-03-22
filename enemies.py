import pygame as pg

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.Surface((48,48)).convert_alpha()
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)

        # movement
        self.direction = pg.math.Vector2()
        self.speed = 5

    def line_move(self):
        self.direction = (-1, 0)
        self.rect.x += self.direction[0] * self.speed

    def bouncy_move(self):
        if self.rect.centerx <= 0 or self.direction == (0,0):
            self.direction = ((1,0))
        elif self.rect.centerx >= 1280:
            self.direction = ((-1,0))
        else:
            pass

        self.rect.x += self.direction[0] * self.speed

    def destroy_enemy(self):
        if self.rect.centerx <= -50 or self.rect.centerx >= 1300:
            print('enemy died by boundaries')
            self.kill()

    def update(self):
        self.line_move()
        self.destroy_enemy()       
        

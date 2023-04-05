import pygame as pg
import math

# player bullets

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, groups, speed, direction: pg.math.Vector2):
        super().__init__(groups)
        self.image = pg.Surface((5, 5)).convert_alpha()
        self.color = 'white'
        self.rect = self.image.get_rect(center = pos)   
        self.direction = direction
        self.speed = speed

    def trajectory(self):
        self.direction = pg.math.Vector2(self.direction)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.centerx += self.direction[0] * self.speed
        self.rect.centery += self.direction[1] * self.speed

    def remove_bullet(self):
        if self.rect.centery <= 0 or self.rect.centery >= 720:
            self.kill()

    def color_bullet(self):
        self.image.fill(self.color)

    def update(self):
        self.trajectory()
        self.remove_bullet()
        self.color_bullet()

class WaveyBullet1(Bullet):
    def __init__(self, pos, groups, speed, direction):
        super().__init__(pos, groups, speed, direction)
        self.color = 'white'
        self.speed = speed
        self.direction = direction
        
    def trajectory(self):
        self.rect.centerx += self.direction[0] * self.speed
        self.rect.centery += self.direction[1] * self.speed
        self.rect.centerx += math.sin(pg.time.get_ticks()/40)*4

class WaveyBullet2(Bullet):
    def __init__(self, pos, groups, speed, direction):
        super().__init__(pos, groups, speed, direction)
        self.speed = speed
        self.direction = direction
        self.color = 'white'
        
    def trajectory(self):
        self.rect.centerx += self.direction[0] * self.speed
        self.rect.centery += self.direction[1] * self.speed
        self.rect.centerx += math.sin(-pg.time.get_ticks()/40)*4

# enemy bullets

class EnemyBullet(Bullet):
    def __init__(self, pos, groups, speed, direction):
        super().__init__(pos, groups, speed, direction)
        self.speed = speed
        self.direction = direction
        self.color = 'yellow'
        

    def trajectory(self):
        self.rect.centerx += self.direction[0] * self.speed
        self.rect.centery += self.direction[1] * self.speed
import pygame as pg
import math
from settings import *

# player bullets

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, groups, speed, direction: pg.math.Vector2):
        super().__init__(groups)
        self.image = pg.Surface((8, 8)).convert_alpha()
        self.color = 'white'
        self.rect = self.image.get_rect(center = pos)   
        self.direction = direction
        self.speed = speed
        self.pos = pg.math.Vector2(self.rect.center)

    def trajectory(self):
        self.direction = pg.math.Vector2(self.direction)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.centerx += self.direction[0] * self.speed
        self.rect.centery += self.direction[1] * self.speed

    def remove_bullet(self):
        if self.rect.centery <= 0 or self.rect.centery >= SCREEN_HEIGHT or self.rect.centerx <=0 or self.rect.centerx >= SCREEN_WIDTH:
            self.kill()

    def color_bullet(self):
        self.image.fill(self.color)

    def aim_bullet(self, destination):
        distance = math.sqrt(pow((self.pos[0] - destination[0]), 2) + pow((self.pos[1] - destination[1]), 2))
        directionx = (destination[0] - self.pos[0])/distance
        directiony = (destination[1] - self.pos[1])/distance
        self.direction = pg.math.Vector2(directionx, directiony)

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
        self.pos.x += self.direction[0] * self.speed
        self.pos.y += self.direction[1] * self.speed
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)


# multi-shot

class ShotsFired:
    def __init__(self, pos, groups, direction, speed, number_of_bullets: int, spread: float):
        self.pos = pos
        self.groups = groups
        self.direction = pg.math.Vector2(direction)
        self.speed = speed
        self.number_of_bullet = list(range(0, number_of_bullets))
        self.shot_switch = True

    def shoot(self):
        if self.shot_switch:
            EnemyBullet(self.pos, self.groups, self.speed, self.direction)
            self.shot_switch = False 

    def update(self):
        self.shoot()
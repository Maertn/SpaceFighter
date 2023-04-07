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
        self.direction = direction
        self.speed = speed
        self.list_of_bullets = list(range(1, number_of_bullets + 1))
        self.shot_switch = True
        
        # creating spread over unit circle
        self.spread = math.pi*2*(spread)
        self.angle = 0
        if number_of_bullets > 1:
            self.angle = self.spread / number_of_bullets
        self.bullet_dict = {}
        
        for bullet in self.list_of_bullets:
            if bullet > 1:
                rotation_index = divmod(bullet,2)
                k = rotation_index[0]
                if rotation_index[1] == 0: 
                    direction = pg.math.Vector2(self.direction)
                    direction = direction.rotate_rad(k * self.angle)
                    direction = (direction[0], direction[1])
                    self.bullet_dict[bullet] = direction
                else:
                    direction = pg.math.Vector2(self.direction)
                    direction = direction.rotate_rad(k * -self.angle)
                    direction = (direction[0], direction[1])
                    self.bullet_dict[bullet] = direction
            else: 
                direction = self.direction
                self.bullet_dict[bullet] = direction
        
        print(self.bullet_dict)
                 
        

    def shoot(self):

        if self.shot_switch:
            for bullet in self.bullet_dict.items():
                
                direction = bullet[1]
                print(direction)
                direction = pg.math.Vector2(direction).normalize()
                
                EnemyBullet(self.pos, self.groups, self.speed, direction)


            self.shot_switch = False 

    def update(self):
        self.shoot()
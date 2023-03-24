import pygame as pg
import math

from settings import *
from bullets import EnemyBullet


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, groups, speed, spawn_time):
        super().__init__(groups)
        self.image = pg.Surface((32,32)).convert_alpha()
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)
        self.spawn_time = spawn_time

        # movement
        self.direction = pg.math.Vector2()
        self.speed = speed

        self.fire_bullet = False

    def line_move(self):
        self.direction = (-1,0)
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def bouncy_move(self):
        if self.rect.centerx <= 0 or self.direction == (0,0):
            self.direction = ((1,0))
        elif self.rect.centerx >= 1280:
            self.direction = ((-1,0))
        else:
            pass

        self.rect.x += self.direction[0] * self.speed

    def circle_move(self):
        self.direction = (-1,0)
        self.rect.centerx += ((math.cos(pg.time.get_ticks()/150)) * self.speed) 
        self.rect.centery += ((math.sin(pg.time.get_ticks()/150)) * self.speed)

    def destroy_enemy(self):
        if self.rect.centerx <= GAME_SCREEN_LEFT - 50 or self.rect.centerx >= GAME_SCREEN_RIGHT + 50:
            self.kill()

    def spawn_bullets(self):
        i = int(pg.time.get_ticks() / 10)
        if i % 2 == 0:
            self.fire_bullet = True
        else:
            self.fire_bullet = False

    def update(self):
        self.destroy_enemy()
        self.spawn_bullets()
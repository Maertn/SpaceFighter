import pygame as pg
import math

from settings import *


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, groups, speed, direction, spawn_time, health, **movement_switch1):
        super().__init__(groups)

        self.image = pg.Surface((32,32)).convert_alpha()
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)
        
        self.spawn_time = spawn_time

        # movement
        self.direction = pg.math.Vector2(direction).normalize()
        self.speed = speed
        self.movement_switch1 = movement_switch1

        # combat attributes
        self.fire_bullet = False
        self.health = health

    def line_move(self):
        self.rect.center += self.direction * self.speed

    def bouncy_move(self):
        if self.rect.centerx <= 0 or self.direction == (0,0):
            self.direction = ((1,0))
        elif self.rect.centerx >= 1280:
            self.direction = ((-1,0))
        else:
            pass

        self.rect.x += self.direction[0] * self.speed

    def circle_move(self):
        self.rect.centerx += (math.cos(((pg.time.get_ticks()/100)-self.spawn_time)/1.5)) * self.speed 
        self.rect.centery += (math.sin(((pg.time.get_ticks()/100)-self.spawn_time)/1.5)) * self.speed

    # doesn't work as intended
    def butterfly_move(self):
        t = ((pg.time.get_ticks()/10) - self.spawn_time) / 10
        print(t)
        """Parametric equations for the butterfly curve"""
        x = math.sin(t) * ((math.exp(math.cos(t)) - (2*(math.cos(4*t)) + pow(math.sin(t/12),5))))
        y = math.cos(t) * ((math.exp(math.cos(t)) - (2*(math.cos(4*t)) + pow(math.sin(t/12),5))))

        self.direction = pg.math.Vector2(x,y)
        self.rect.center += self.direction * self.speed * 10 # might need tweaking
         
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
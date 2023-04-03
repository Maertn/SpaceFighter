import pygame as pg
import math

from settings import *


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, groups, speed, direction, spawn_time, health, **movement_switch):
        super().__init__(groups)

        self.image = pg.Surface((32,32)).convert_alpha()
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)
        
        self.spawn_time = spawn_time

        # movement
        self.direction = pg.math.Vector2(direction).normalize()
        self.speed = speed
        try:
            self.movement_switch1 = movement_switch["movement_switch1"]
        except:
            pass
        try:
            self.movement_switch2 = movement_switch["movement_switch2"]
        except:
            pass
        try:
            self.movement_switch3 = movement_switch["movement_switch3"]
        except:
            pass

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

    def move_to(self, destination, speed):
        distance = math.sqrt(pow((self.rect.centerx - destination[0]),2) + pow((self.rect.centery - destination[1]),2))
        if distance != 0:
            self.direction = pg.math.Vector2(((destination[0] - self.rect.centerx)/distance), ((destination[1] - self.rect.centery)/distance))
        else:
            self.rect.center = destination

        if self.rect.centerx - destination[0] <= 0:
            if self.rect.centery - destination[1] <= 0:
                if not (self.rect.centerx >= destination[0] and self.rect.centery >= destination[1]):
                    self.rect.centerx += self.direction[0] * speed
                    self.rect.centery += self.direction[1] * speed
                else:
                    self.rect.center = destination
            
            else:
                if not (self.rect.centerx >= destination[0] and self.rect.centery <= destination[1]):
                    self.rect.centerx += self.direction[0] * speed
                    self.rect.centery += self.direction[1] * speed
                else:
                    self.rect.center = destination
        
        else:
            if self.rect.centery - destination[1] <= 0:
                if not (self.rect.centerx <= destination[0] and self.rect.centery >= destination[1]):
                    self.rect.centerx += self.direction[0] * speed
                    self.rect.centery += self.direction[1] * speed
                else:
                    self.rect.center = destination

            else:
                if not (self.rect.centerx <= destination[0] and self.rect.centery <= destination[1]):
                    self.rect.centerx += self.direction[0] * speed
                    self.rect.centery += self.direction[1] * speed
                else:
                    self.rect.center = destination

    def update(self):
        self.destroy_enemy()
        # self.spawn_bullets()
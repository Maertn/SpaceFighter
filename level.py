import pygame as pg
import time

from settings import *
from player import Player
from bullets import Bullet
from enemies import Enemy

class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pg.display.get_surface()

        # sprite groups
        self.visible_sprites = pg.sprite.Group()
        self.obstacle_sprites = pg.sprite.Group()

        # sprite setup
        self.create_map()

        self.spawn_switch = None

    def create_map(self):
        x = WIDTH // 2
        y = HEIGHT // 2
        self.player = Player((x,y), [self.visible_sprites])

    def spawn_enemies(self):
        i = int(pg.time.get_ticks() / 1000)
        if int(i % 2) == 0 and not self.spawn_switch:
            self.spawn_switch = True
        elif int(i % 2) == 1 and self.spawn_switch:
            Enemy((WIDTH, HEIGHT // 2 - 300), [self.visible_sprites])
            self.spawn_switch = False
                


    

    def shoot_stuff(self, player):
        if self.player.shooting and not self.player.dodging:
            x = self.player.rect.centerx
            y = self.player.rect.top
            Bullet((x,y), [self.visible_sprites])
            print('shooting')
            

    def run(self):
        self.shoot_stuff(self.player)
        self.spawn_enemies()
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        
        
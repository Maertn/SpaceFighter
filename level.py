import pygame as pg
from settings import *
from player import Player
from bullets import Bullet

class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pg.display.get_surface()

        # sprite groups
        self.visible_sprites = pg.sprite.Group()
        self.obstacle_sprites = pg.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        x = WIDTH // 2
        y = HEIGHT // 2
        player = Player((x,y), [self.visible_sprites])
    
    def spawn_bullets(self):
        if self.player.status = 'shooting'

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        
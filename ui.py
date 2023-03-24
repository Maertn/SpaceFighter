import pygame as pg
from settings import *

class UI:
    def __init__(self):

        # general
        self.display_surface = pg.display.get_surface()
        
        # border setup
        self.left_border = pg.Rect(0, 0, GAME_SCREEN_LEFT, SCREEN_HEIGHT)
        self.right_border = pg.Rect(GAME_SCREEN_RIGHT, 0, GAME_SCREEN_LEFT, SCREEN_HEIGHT)

    def draw_border(self):
        pg.draw.rect(self.display_surface, BORDER_COLOR, self.left_border)
        pg.draw.rect(self.display_surface, BORDER_COLOR, self.right_border)

    def display(self):
        self.draw_border()

import pygame as pg
from settings import *

class UI:
    def __init__(self):

        # general
        self.display_surface = pg.display.get_surface()
        
        # border setup
        self.left_border = pg.Rect(0, 0, GAME_SCREEN_LEFT, SCREEN_HEIGHT)
        self.right_border = pg.Rect(GAME_SCREEN_RIGHT, 0, GAME_SCREEN_LEFT, SCREEN_HEIGHT)

        # score setup

        self.score_font = pg.font.Font(SCORE_FONT, 20)
        self.score_surf = None
        self.score_rect = None

    def draw_border(self):
        pg.draw.rect(self.display_surface, BORDER_COLOR, self.left_border)
        pg.draw.rect(self.display_surface, BORDER_COLOR, self.right_border)

    def display_score(self):
        self.current_score = int(pg.time.get_ticks()/1000)
        self.score_surf = self.score_font.render(f'Hi-Score: {self.current_score}', False, 'black')
        self.score_rect = self.score_surf.get_rect(center = (GAME_SCREEN_LEFT / 2, 100))
        self.display_surface.blit(self.score_surf, self.score_rect)

    def display(self):
        self.draw_border()
        self.display_score()
        

class Menu:
    def __init__(self):
        # general
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font(TITLE_FONT, TITLE_FONT_SIZE)

        # border setup
        self.menu = pg.Rect(GAME_SCREEN_LEFT, 0, SCREEN_WIDTH / 5 * 3, SCREEN_HEIGHT)

    def draw_menu(self):
        pg.draw.rect(self.display_surface, TITLE_COLOR, self.menu)


class MainMenu(Menu):
    def show_main_menu_text(self):
        text_surf = self.font.render('SpaceFighter', False, TITLE_TEXT_COLOR)
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 - 200
        text_rect = text_surf.get_rect(center = (x,y))

        pg.draw.rect(self.display_surface, TITLE_COLOR, text_rect)
        self.display_surface.blit(text_surf, text_rect)

    def display(self):
        self.draw_menu()
        self.show_main_menu_text()


class GameOver(Menu):
    def show_game_over_text(self):
        text_surf = self.font.render('You Died', False, TITLE_TEXT_COLOR)
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 - 200
        text_rect = text_surf.get_rect(center = (x,y))
        
        pg.draw.rect(self.display_surface, TITLE_COLOR, text_rect)
        self.display_surface.blit(text_surf, text_rect)

    def display(self):
        self.draw_menu()
        self.show_game_over_text()
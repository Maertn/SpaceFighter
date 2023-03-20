import pygame as pg
import sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('SpaceFighter')

        self.level = Level()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.level.run()
            pg.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
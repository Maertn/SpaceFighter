import pygame as pg
import math, sys

class TestPath(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        
        
        self.image = pg.Surface((2,2)).convert_alpha()
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)

    def butterfly_move(self):
        t = math.radians(pg.time.get_ticks() / 5)

        """Parametric equations for the butterfly curve"""
        x = math.sin(t) * ((math.exp(math.cos(t)) - (2*(math.cos(4*t)) + pow(math.sin(t/12),5))))
        y = math.cos(t) * ((math.exp(math.cos(t)) - (2*(math.cos(4*t)) + pow(math.sin(t/12),5))))

        self.direction = pg.math.Vector2(x,y)
        self.rect.center += -self.direction * 60

        print(int(t/10)/10, self.rect.x, self.rect.y)

    def update(self):
        self.butterfly_move()
        

class TestSuite:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1280, 720))
        pg.display.set_caption('TestSuite')
        self.clock = pg.time.Clock()
        self.display_surface = pg.display.get_surface()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            self.visible_sprites = pg.sprite.Group()

            test = TestPath((640, 360), [self.visible_sprites])

            test.update()
            self.visible_sprites.draw(self.display_surface)
            self.visible_sprites.update()
            pg.display.update()
            self.clock.tick(120)

if __name__ == '__main__':
    suite = TestSuite()
    suite.run()

import pygame as pg
import math, sys

class TestPath(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        
        
        self.image = pg.Surface((2,2)).convert_alpha()
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)

    def butterfly_move(self):
        t = pg.time.get_ticks() / 10
        
        """Parametric equations for the butterfly curve"""
        self.rect.x += 20*math.sin(math.radians(t)) * ((math.exp(math.cos(math.radians(t)) - (2*(math.cos(4*math.radians(t))) + pow(math.sin(math.radians(t)/12),5)))))
        self.rect.y += 20*math.cos(math.radians(t)) * ((math.exp(math.cos(math.radians(t)) - (2*(math.cos(4*math.radians(t))) + pow(math.sin(math.radians(t)/12),5)))))

        print(int(t/10)/100, self.rect.x, self.rect.y)

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
            self.clock.tick(60)

if __name__ == '__main__':
    suite = TestSuite()
    suite.run()

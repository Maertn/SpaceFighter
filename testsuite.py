import pygame as pg
import math, sys

class TestPath(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        
        self.display_surface = pg.display.get_surface()
        self.image = pg.Surface((2,2)).convert_alpha()
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)

    def butterfly_move(self):
        t = math.radians(pg.time.get_ticks() / 5)

        """Parametric equations for the butterfly curve"""
        x = math.sin(t) * ((math.exp(math.cos(t)) - (2*(math.cos(4*t)) + pow(math.sin(t/12),5))))
        y = math.cos(t) * ((math.exp(math.cos(t)) - (2*(math.cos(4*t)) + pow(math.sin(t/12),5))))

        self.direction = pg.math.Vector2(x,y)
        self.rect.center += self.direction * 60

        print(int(t/10)/10, self.rect.x, self.rect.y)
    
    def unit_circle_by_five(self):
        
        t = pg.time.get_ticks()

        x0 = 360
        y0 = 360

        k = 2 * math.pi

        position1 = (math.sin(k * 5/5), -math.cos(k * 5/5))
        position2 = (math.sin(k * 1/5), -math.cos(k * 1/5))
        position3 = (math.sin(k * 2/5), -math.cos(k * 2/5))
        position4 = (math.sin(k * 3/5), -math.cos(k * 3/5))
        position5 = (math.sin(k * 4/5), -math.cos(k * 4/5))

        if t%10 == 0:
            self.rect.center = (x0 + (20 * position1[0])),  y0 + (20 * position1[1])
        if t%10 == 1:
            self.rect.center = (x0 + (20 * position2[0])),  y0 + (20 * position2[1])
        if t%10 == 2:
            self.rect.center = (x0 + (20 * position3[0])),  y0 + (20 * position3[1])
        if t%10 == 3:
            self.rect.center = (x0 + (20 * position4[0])),  y0 + (20 * position4[1])
        if t%10 == 4:
            self.rect.center = (x0 + (20 * position5[0])),  y0 + (20 * position5[1])


    def update(self):
        self.unit_circle_by_five()
        

class TestSuite:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((720, 720))
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

            test = TestPath((360, 360), [self.visible_sprites])

            test.update()
            self.visible_sprites.draw(self.display_surface)
            self.visible_sprites.update()
            pg.display.update()
            self.clock.tick(120)

if __name__ == '__main__':
    suite = TestSuite()
    suite.run()

import pygame as pg
from random import randint

from settings import *
from player import Player
from bullets import Bullet, EnemyBullet
from enemies import Enemy

class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pg.display.get_surface()

        # sprite groups
        self.visible_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.obstacle_sprites = pg.sprite.Group()
        self.enemy_bullet_sprites = pg.sprite.Group()
        self.player_bullets_sprites = pg.sprite.Group()
        self.player_alive = True

        # sprite setup
        self.create_map()

        # enemy behaviour switches
        self.spawn_switch = None
        self.enemy_fire_switch = None

        # player behaviour switches
        self.shoot_stuff_timer = 0
        self.shoot_stuff_cooldown = 200
        self.shoot_stuff_switch = True

    def create_map(self):
        x = WIDTH // 2
        y = HEIGHT // 2
        self.player = Player((x,y), [self.visible_sprites])

    def spawn_enemies(self):
        i = int(pg.time.get_ticks() / 1000)
        if int(i % 2) == 0 and not self.spawn_switch:
            self.spawn_switch = True
        elif int(i % 2) == 1 and self.spawn_switch:
            Enemy((WIDTH, HEIGHT // 2 - 300), [self.visible_sprites, self.enemy_sprites])
            self.spawn_switch = False

    def shoot_stuff(self, player):
        if self.shoot_stuff_switch and self.player.shooting and not self.player.dodging and self.player_alive:
            x = self.player.rect.centerx
            y = self.player.rect.top
            Bullet((x,y), [self.visible_sprites, self.player_bullets_sprites])
            print('bullet')
            self.shoot_stuff_switch = False
            self.shoot_stuff_timer = pg.time.get_ticks()

    def enemy_fire(self):
        for enemy in self.enemy_sprites:
            enemy_fire_switch = None
            i = pg.time.get_ticks() 
            x = enemy.rect.centerx
            y = enemy.rect.centery
            if (int(i % 10) == 5 + randint(-5,5)) and not self.spawn_switch:
                enemy_fire_switch = True
            if enemy_fire_switch and enemy.fire_bullet:
                enemy.fire_bullet = False
                EnemyBullet((x,y), [self.visible_sprites, self.enemy_bullet_sprites])
    
    def collisions(self, player):
        for bullet in self.player_bullets_sprites:
            for enemy in self.enemy_sprites:
                if bullet.rect.centerx in range(enemy.rect.left,enemy.rect.right) and bullet.rect.centery in range(enemy.rect.top, enemy.rect.bottom):
                    enemy.kill()
                    bullet.kill()

        for bullet in self.enemy_bullet_sprites:
            if bullet.rect.centerx in range(player.rect.left,player.rect.right) and bullet.rect.centery in range(player.rect.top, player.rect.bottom) and not self.player.dodging:
                player.kill()
                bullet.kill()
                self.player_alive = False
        
        for enemy in self.enemy_sprites:
            if enemy.rect.centerx in range(player.rect.left,player.rect.right) and enemy.rect.centery in range(player.rect.top, player.rect.bottom) and not self.player.dodging:
                player.kill()
                self.player_alive = False

    def cooldowns(self):
        current_time = pg.time.get_ticks()
        if not self.shoot_stuff_switch and current_time - self.shoot_stuff_timer >= self.shoot_stuff_cooldown:
            self.shoot_stuff_switch = True
            

    def run(self):
        self.shoot_stuff(self.player)
        self.spawn_enemies()
        self.enemy_fire()
        self.collisions(self.player)
        self.cooldowns()
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        
        
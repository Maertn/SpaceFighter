import pygame as pg
from random import randint
import math

from settings import *
from ui import UI, MainMenu, GameOver
from player import Player
from bullets import Bullet, EnemyBullet, WaveyBullet1, WaveyBullet2
from enemies import Enemy
from powerup import PowerUp

class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pg.display.get_surface()

        # borders / menu
        self.ui = UI()
        self.main_menu = MainMenu()
        self.title_screen = True
        self.game_over = GameOver()

        # hi-score
        self.minus_score_time = 0
        self.score_time = 0
        self.kill_count = 0

        # sprite groups
        self.visible_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.enemy_bullet_sprites = pg.sprite.Group()
        self.player_bullets_sprites = pg.sprite.Group()
        self.power_up_sprites = pg.sprite.Group()

        self.list_of_sprite_groups = [
                    self.visible_sprites,
                    self.enemy_sprites,
                    self.enemy_bullet_sprites,
                    self.player_bullets_sprites,
                    self.power_up_sprites
                    ]

        # player sprite setup
        self.create_map()

        # enemy behaviour switches
        self.spawn_switch_right = True
        self.spawn_switch_left = True
        self.enemy_fire_switch = None

        # player behaviour switches
        self.shoot_stuff_timer = 0
        self.shoot_stuff_cooldown = 50
        self.shoot_stuff_switch = True

        # power ups
        self.power_up_timer = 0
        self.power_up_spawn_switch = True
        self.power_up_switch_cooldown = 1100
        self.power_up_wave_timer = 0
        self.power_up_wave_switch = True
        self.power_up_wave_cooldown = 8000

    def create_map(self):
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2 + 300
        self.player = Player((x,y), [self.visible_sprites])
        self.minus_score_time = -int(pg.time.get_ticks()/1000)

    def spawn_enemies(self):
        """A function used in testing to spawn enemies ever 2 seconds."""
        t = int(pg.time.get_ticks() / 1000)
        spawn_time = pg.time.get_ticks() / 10
        
        # Enemies from the right
        if int(t % 2) == 0 and not self.spawn_switch_right:
            self.spawn_switch_right = True
        elif int(t % 2) == 1 and self.spawn_switch_right:
            Enemy((GAME_SCREEN_RIGHT, SCREEN_HEIGHT * 2 / 3), [self.visible_sprites, self.enemy_sprites], -3, (math.cos(-math.pi/6), -2*math.sin(-math.pi/6)), spawn_time, True)
            self.spawn_switch_right = False

        # Enemies from the left
        if int(t % 2) == 0 and not self.spawn_switch_left:
            self.spawn_switch_left = True
        elif int(t % 2) == 1 and self.spawn_switch_left:
            Enemy((GAME_SCREEN_LEFT, SCREEN_HEIGHT * 2 / 3), [self.visible_sprites, self.enemy_sprites], 3, (math.cos(math.pi/6), -2*math.sin(math.pi/6)), spawn_time, True)
            self.spawn_switch_left = False


    def spawn_power_ups(self):
        """A function used in testing that spawns power-ups every 5 seconds."""
        current_time = int(pg.time.get_ticks()/1000)
        current_time_in_ms = pg.time.get_ticks()
        if current_time % 10 == 0 and self.power_up_spawn_switch and self.player.fire_pattern <2:
            PowerUp((randint(GAME_SCREEN_LEFT, GAME_SCREEN_RIGHT), 0), [self.visible_sprites, self.power_up_sprites], 'power_up_shots', 'green')
            self.power_up_spawn_switch = False
            self.power_up_timer = current_time_in_ms
        if current_time % 10 == 5 and self.power_up_spawn_switch and not self.player.wave_pattern:
            PowerUp((randint(GAME_SCREEN_LEFT, GAME_SCREEN_RIGHT), 0), [self.visible_sprites, self.power_up_sprites], 'power_up_wave', 'purple')
            self.power_up_spawn_switch = False
            self.power_up_timer = current_time_in_ms            

    
    def enemy_patterns(self):
        """A function used in testing that describes a sequence of motion for enemy sprites"""
        current_time = int(pg.time.get_ticks() / 10)
        for i, enemy in enumerate(self.enemy_sprites):
            #print(i, enemy.rect.center)
            if current_time - enemy.spawn_time <= 200:
                enemy.line_move()
            elif current_time - enemy.spawn_time <= 300:
                enemy.circle_move()
            elif current_time - enemy.spawn_time <= 600:
                if enemy.movement_switch1 and enemy.speed > 0:
                    enemy.movement_switch1 = False
                    enemy.direction = enemy.direction.rotate(-90)
                if enemy.movement_switch1 and enemy.speed < 0:
                    enemy.movement_switch1 = False
                    enemy.direction = enemy.direction.rotate(90)
                enemy.line_move()
            else:
                enemy.kill()

    def shoot_stuff(self, player):
        if self.shoot_stuff_switch and self.player.shooting and not self.player.dodging and self.player.alive:
            x = self.player.rect.centerx
            y = self.player.rect.top
            
            if player.fire_pattern == 0 and not player.wave_pattern:
                Bullet((x,y), [self.visible_sprites, self.player_bullets_sprites])
                
            if player.fire_pattern == 1 and not player.wave_pattern:
                bullet1 = Bullet((x-16,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet2 = Bullet((x+16,y), [self.visible_sprites, self.player_bullets_sprites])

            if player.fire_pattern == 2 and not player.wave_pattern:
                bullet1 = Bullet((x-16,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet1.direction = pg.math.Vector2((math.sin(math.pi/12), 1))
                bullet2 = Bullet((x,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet3 = Bullet((x+16,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet3.direction = pg.math.Vector2((math.sin(-math.pi/12), 1))

            if player.fire_pattern == 0 and player.wave_pattern:
                bullet1_1 = WaveyBullet1((x,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet1_2 = WaveyBullet2((x,y), [self.visible_sprites, self.player_bullets_sprites])

            if player.fire_pattern == 1 and player.wave_pattern:
                bullet1_1 = WaveyBullet1((x-16,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet1_2 = WaveyBullet2((x-16,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet2_1 = WaveyBullet1((x+16,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet2_2 = WaveyBullet2((x+16,y), [self.visible_sprites, self.player_bullets_sprites])

            if player.fire_pattern == 2 and player.wave_pattern:
                bullet1_1 = WaveyBullet1((x-16,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet1_1.direction = pg.math.Vector2((math.sin(math.pi/12), 1))
                bullet1_2 = WaveyBullet2((x-16,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet1_2.direction = pg.math.Vector2((math.sin(math.pi/12), 1))
                bullet2_1 = WaveyBullet1((x,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet2_2 = WaveyBullet2((x,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet3_1 = WaveyBullet1((x+16,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet3_1.direction = pg.math.Vector2((math.sin(-math.pi/12), 1))
                bullet3_2 = WaveyBullet2((x+32,y), [self.visible_sprites, self.player_bullets_sprites])
                bullet3_2.direction = pg.math.Vector2((math.sin(-math.pi/12), 1))

            self.shoot_stuff_switch = False
            self.shoot_stuff_timer = pg.time.get_ticks()

    def enemy_fire(self):
        """Used in testing. Makes all enemies fire a bullet at random intervals"""
        for enemy in self.enemy_sprites:
            enemy_fire_switch = None
            i = pg.time.get_ticks() 
            x = enemy.rect.centerx
            y = enemy.rect.centery
            if (int(i % 10) == 5 + randint(-5,5)) and not enemy_fire_switch:
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
                    self.kill_count += 1
                    
        for bullet in self.enemy_bullet_sprites:
            if bullet.rect.centerx in range(player.rect.left,player.rect.right) and bullet.rect.centery in range(player.rect.top, player.rect.bottom) and not self.player.dodging:
                player.kill()
                bullet.kill()
                self.player.alive = False
        
        for enemy in self.enemy_sprites:
            if enemy.rect.centerx in range(player.rect.left,player.rect.right) and enemy.rect.centery in range(player.rect.top, player.rect.bottom) and not self.player.dodging:
                player.kill()
                self.player.alive = False

        for power_up in self.power_up_sprites:
            if power_up.rect.centerx in range(player.rect.left,player.rect.right) and power_up.rect.centery in range(player.rect.top, player.rect.bottom):
                if power_up.upgrade == 'power_up_shots' and player.fire_pattern <2: 
                    player.fire_pattern += 1
                    power_up.kill()
                if power_up.upgrade == 'power_up_wave' and self.power_up_spawn_switch:
                    player.wave_pattern = True
                    self.power_up_wave_switch = False
                    power_up.kill()
                    self.power_up_wave_timer = pg.time.get_ticks()
                    

    def cooldowns(self, player):
        current_time = pg.time.get_ticks()
        if not self.shoot_stuff_switch and current_time - self.shoot_stuff_timer >= self.shoot_stuff_cooldown:
            self.shoot_stuff_switch = True

        if not self.power_up_spawn_switch and current_time - self.power_up_switch_cooldown >= self.power_up_timer:
            self.power_up_spawn_switch = True

        if not self.power_up_wave_switch and current_time - self.power_up_wave_cooldown >= self.power_up_wave_timer:
            self.power_up_wave_switch = True
            player.wave_pattern = False
            print(True)
            
    def create_time_score(self):
        self.score_time = int(pg.time.get_ticks()/1000) + self.minus_score_time  

    def keylog(self):
        keys = pg.key.get_pressed()
        if not self.player.alive:
            if keys[pg.K_SPACE]:
                self.title_screen = False
                self.create_map()
                self.kill_count = 0
                self.player.alive = True

    def run(self):
        if self.player.alive:
            self.create_time_score()
            self.shoot_stuff(self.player)
            self.spawn_power_ups()
            self.spawn_enemies()
            self.enemy_fire()
            self.enemy_patterns()
            self.collisions(self.player)
            self.cooldowns(self.player)
            self.visible_sprites.draw(self.display_surface)
            self.visible_sprites.update()
            self.ui.display()
            self.ui.display_score(self.score_time, self.kill_count)
        else:
            # removing the sprites after death
            for sprite_group in self.list_of_sprite_groups:
                if sprite_group:
                    sprite_group.empty()
            
            if self.title_screen == True:
                self.ui.display()
                self.main_menu.display()
            else:
                self.ui.display()
                self.game_over.display()
        self.keylog()
        
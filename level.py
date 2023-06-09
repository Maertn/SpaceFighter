import pygame as pg
from random import randint
import math
import time

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
        self.death_screen_cooldown = 700
        self.death_screen_switch = False
        self.death_screen_timer = 0

        # hi-score
        self.minus_score_time = 0
        self.score_time = 0
        self.kill_count = 0

        # enemy behaviour switch
        self.enemy_spawn_switch1 = True
        self.enemy_spawn_switch2 = True

        # sprite groups
        self.visible_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.enemy_bullet_sprites = pg.sprite.Group()
        self.player_bullets_sprites = pg.sprite.Group()
        self.power_up_sprites = pg.sprite.Group()
        self.enemy_group1 = pg.sprite.Group()
        self.enemy_group2 = pg.sprite.Group()

        self.list_of_sprite_groups = [
                    self.visible_sprites,
                    self.enemy_sprites,
                    self.enemy_bullet_sprites,
                    self.player_bullets_sprites,
                    self.power_up_sprites
                    ]

        # player sprite setup
        self.create_map()

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

        # enemy behaviour switches
        self.spawn_switch_right = True
        self.spawn_switch_left = True
        self.enemy_fire_switch = None

    def create_map(self):
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2 + 300
        self.player = Player((x,y), [self.visible_sprites])
        self.minus_score_time = -int(pg.time.get_ticks()/1000)

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

    def enemies(self):
        spawn_time = pg.time.get_ticks() / 10
       
        # Creating positions for a 5-pointed star
        k = math.pi * 2
        position1 = ((SCREEN_WIDTH/2) + (120*math.sin(k * 5/5)), (SCREEN_HEIGHT/2)+(120*-math.cos(k * 5/5)))
        position2 = ((SCREEN_WIDTH/2) + (120*math.sin(k * 1/5)), (SCREEN_HEIGHT/2)+(120*-math.cos(k * 1/5)))
        position3 = ((SCREEN_WIDTH/2) + (120*math.sin(k * 2/5)), (SCREEN_HEIGHT/2)+(120*-math.cos(k * 2/5)))
        position4 = ((SCREEN_WIDTH/2) + (120*math.sin(k * 3/5)), (SCREEN_HEIGHT/2)+(120*-math.cos(k * 3/5)))
        position5 = ((SCREEN_WIDTH/2) + (120*math.sin(k * 4/5)), (SCREEN_HEIGHT/2)+(120*-math.cos(k * 4/5)))

        # Spawn one enemy
        if self.enemy_spawn_switch1 == True:
            enemy = Enemy( 
            pos=position1, 
            groups=[self.visible_sprites, self.enemy_sprites], 
            speed=0, 
            direction=(0,1), 
            spawn_time=spawn_time, 
            health=1,
            movement_switch1 = True,
            movement_switch2 = True,
            movement_switch3 = True,
            movement_switch4 = True,
            movement_switch5 = True
            )
            self.enemy_spawn_switch1 = False

        # Instructions for movement along the points of a 5-pointed star
        for enemy in self.enemy_sprites:
            destination = enemy.rect.center
            bullet = None
            if enemy.movement_switch1:
                destination = position3
                enemy.move_to(destination, speed = 5)
                if ((enemy.rect.centerx >= destination[0] + 1) or (enemy.rect.centerx >= destination[0] - 1)) or enemy.rect.centery >= destination[1]:
                    
                    bullet1 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet2 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet3 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet1.aim_bullet(self.player.rect.center)
                    bullet2.aim_bullet((self.player.rect.centerx + 50, self.player.rect.centery + 50))
                    bullet3.aim_bullet((self.player.rect.centerx - 50, self.player.rect.centery - 50))
                    
                    enemy.movement_switch1 = False

            
            elif enemy.movement_switch2 and not enemy.movement_switch1:
                destination = position5
                enemy.move_to(destination, speed = 5)
                if enemy.rect.centerx <= destination[0]:
                   
                    bullet1 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet2 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet3 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet1.aim_bullet(self.player.rect.center)
                    bullet2.aim_bullet((self.player.rect.centerx + 50, self.player.rect.centery + 50))
                    bullet3.aim_bullet((self.player.rect.centerx - 50, self.player.rect.centery - 50))

                    enemy.movement_switch2 = False

            elif enemy.movement_switch3 and not enemy.movement_switch2:
                destination = position2
                enemy.move_to(destination, speed = 5)
                if (enemy.rect.centerx > destination[0] + 1) or (enemy.rect.centerx > destination[0] - 1):  
                   
                    bullet1 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet2 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet3 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet1.aim_bullet(self.player.rect.center)
                    bullet2.aim_bullet((self.player.rect.centerx + 50, self.player.rect.centery + 50))
                    bullet3.aim_bullet((self.player.rect.centerx - 50, self.player.rect.centery - 50))

                    enemy.movement_switch3 = False
            
            elif enemy.movement_switch4 and not enemy.movement_switch3:
                destination = position4
                enemy.move_to(destination, speed = 5)
                if (enemy.rect.centerx <= destination[0] and enemy.rect.centery >= destination[1]):
                                       
                    bullet1 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet2 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet3 = EnemyBullet(
                        pos = enemy.rect.center, 
                        groups = [self.visible_sprites, self.enemy_bullet_sprites],
                        speed = 1,
                        direction = (0,0)
                    )
                    
                    bullet1.aim_bullet(self.player.rect.center)
                    bullet2.aim_bullet((self.player.rect.centerx + 50, self.player.rect.centery + 50))
                    bullet3.aim_bullet((self.player.rect.centerx - 50, self.player.rect.centery - 50))
                    enemy.movement_switch4 = False
                    
            else:
                destination = position1
                enemy.move_to(destination, speed = 5)

        if int(pg.time.get_ticks() / 100) % 6 == 0:
            print(len(self.visible_sprites), len(self.enemy_bullet_sprites))
        for bullet in self.enemy_bullet_sprites:
            print('--')
            print(bullet.rect.center, bullet.direction)

    def shoot_stuff(self, player):
        if self.shoot_stuff_switch and self.player.shooting and not self.player.dodging and self.player.alive:
            x = self.player.rect.centerx
            y = self.player.rect.top
            
            if player.fire_pattern == 0 and not player.wave_pattern:
                Bullet((x,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                
            if player.fire_pattern == 1 and not player.wave_pattern:
                bullet1 = Bullet((x-16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet2 = Bullet((x+16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))

            if player.fire_pattern == 2 and not player.wave_pattern:
                bullet1 = Bullet((x-16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet1.direction = pg.math.Vector2((math.sin(math.pi/12), 1))
                bullet2 = Bullet((x,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet3 = Bullet((x+16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet3.direction = pg.math.Vector2((math.sin(-math.pi/12), 1))

            if player.fire_pattern == 0 and player.wave_pattern:
                bullet1_1 = WaveyBullet1((x,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet1_2 = WaveyBullet2((x,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))

            if player.fire_pattern == 1 and player.wave_pattern:
                bullet1_1 = WaveyBullet1((x-16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet1_2 = WaveyBullet2((x-16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet2_1 = WaveyBullet1((x+16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet2_2 = WaveyBullet2((x+16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))

            if player.fire_pattern == 2 and player.wave_pattern:
                bullet1_1 = WaveyBullet1((x-16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet1_1.direction = pg.math.Vector2((math.sin(math.pi/12), 1))
                bullet1_2 = WaveyBullet2((x-16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet1_2.direction = pg.math.Vector2((math.sin(math.pi/12), 1))
                bullet2_1 = WaveyBullet1((x,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet2_2 = WaveyBullet2((x,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet3_1 = WaveyBullet1((x+16,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet3_1.direction = pg.math.Vector2((math.sin(-math.pi/12), 1))
                bullet3_2 = WaveyBullet2((x+32,y), [self.visible_sprites, self.player_bullets_sprites], -12, (0,1))
                bullet3_2.direction = pg.math.Vector2((math.sin(-math.pi/12), 1))

            self.shoot_stuff_switch = False
            self.shoot_stuff_timer = pg.time.get_ticks()
    
    def collisions(self, player):
        for bullet in self.player_bullets_sprites:
            for enemy in self.enemy_sprites:
                if bullet.rect.centerx in range(enemy.rect.left,enemy.rect.right) and bullet.rect.centery in range(enemy.rect.top, enemy.rect.bottom):
                    enemy.health -= 1
                    bullet.kill()
                    if enemy.health <=0:
                        self.kill_count += 1
                        enemy.kill()
                    
        for bullet in self.enemy_bullet_sprites:
            if bullet.rect.centerx in range(player.rect.left,player.rect.right) and bullet.rect.centery in range(player.rect.top, player.rect.bottom) and not self.player.dodging:
                player.kill()
                bullet.kill()
                self.player.alive = False
                self.death_screen_timer = pg.time.get_ticks()
                self.death_screen_switch = True

        for enemy in self.enemy_sprites:
            if enemy.rect.centerx in range(player.rect.left,player.rect.right) and enemy.rect.centery in range(player.rect.top, player.rect.bottom) and not self.player.dodging:
                player.kill()
                self.player.alive = False
                self.death_screen_timer = pg.time.get_ticks()
                self.death_screen_switch = True
 
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
        
        # cooldown on player shoot ability
        if not self.shoot_stuff_switch and current_time - self.shoot_stuff_timer >= self.shoot_stuff_cooldown:
            self.shoot_stuff_switch = True

        # cooldown on spawning of bullet upgrades
        if not self.power_up_spawn_switch and current_time - self.power_up_switch_cooldown >= self.power_up_timer:
            self.power_up_spawn_switch = True

        # cooldown on spawning of wavey upgrades 
        if not self.power_up_wave_switch and current_time - self.power_up_wave_cooldown >= self.power_up_wave_timer:
            self.power_up_wave_switch = True
            player.wave_pattern = False

        # cooldown on death screen
        if current_time - self.death_screen_timer >= self.death_screen_cooldown:
            self.death_screen_switch = False
            
    def create_time_score(self):
        self.score_time = int(pg.time.get_ticks()/1000) + self.minus_score_time  

    def start_new_game(self):
        keys = pg.key.get_pressed()
        if not self.player.alive and not self.death_screen_switch:
            if keys[pg.K_SPACE]:
                self.title_screen = False
                self.create_map()
                self.kill_count = 0
                self.player.alive = True
                self.enemy_spawn_switch1 = True

    def run(self):
        self.start_new_game()
        self.cooldowns(self.player)
        if self.player.alive:
            self.enemies()
            self.create_time_score()
            # self.shoot_stuff(self.player)
            # self.spawn_power_ups()
            self.collisions(self.player)
            self.visible_sprites.draw(self.display_surface)
            self.visible_sprites.update()
            self.ui.display()
            self.ui.display_score(self.score_time, self.kill_count)
        else:
            # removing the sprites after death
            for sprite_group in self.list_of_sprite_groups:
                sprite_group.empty()
            
            if self.title_screen == True:
                self.ui.display()
                self.main_menu.display()
            else:
                self.ui.display()
                self.game_over.display()
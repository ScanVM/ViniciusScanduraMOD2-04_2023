import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.birds import Birds
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.time_new_obstacle = 0
        self.choice_dic = 0
        self.hit = 0
    
    def update(self, game):
        
        choice_obstacle = {
            1: Cactus(),
            2: Birds(),
        }
        self.time_new_obstacle = pygame.time.get_ticks()
        
        if self.time_new_obstacle > 5000:
            self.choice_dic = random.randint(1,2)
        else:
            self.choice_dic = 1
        
        if len(self.obstacles) == 0:
            if self.choice_dic == 1:
                self.obstacles.append(choice_obstacle[1])
            elif self.choice_dic == 2:
                self.obstacles.append(choice_obstacle[2])
        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    if self.hit > 0:
                        game.final_score = game.score + (self.hit * 4)
                        game.score = 0
                        break
                    else:
                        game.final_score = game.score
                        game.score = 0
                        break
                else:
                    if game.player.hammer == True:
                        self.hit += 1
                        
                    self.obstacles.remove(obstacle)
    
    def draw (self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def reset_obstacles(self):
        self.obstacles = []
import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.birds import Birds
from dino_runner.utils.constants import SMALL_CACTUS
from dino_runner.utils.constants import LARGE_CACTUS
from dino_runner.utils.constants import BIRD

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.choice_cact = 0
        self.time_new_obstacle = 0
        self.choice_obstacle = 0
    
    def update(self, game):
        self.time_new_obstacle = pygame.time.get_ticks()
        self.choice_cact = random.randint(0,1)
        
        if self.time_new_obstacle > 5000:
            self.choice_obstacle = random.randint(1,2)
        else:
            self.choice_obstacle = 1
        
        if len(self.obstacles) == 0:
            if self.choice_obstacle == 1:
                if self.choice_cact == 0:
                    self.obstacles.append(Cactus(SMALL_CACTUS))
                else:
                    self.obstacles.append(Cactus(LARGE_CACTUS))
            else:
                if self.choice_obstacle == 2:
                    self.obstacles.append(Birds(BIRD))
        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break

    def draw (self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
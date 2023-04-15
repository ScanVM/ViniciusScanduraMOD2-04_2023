import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS
from dino_runner.utils.constants import LARGE_CACTUS

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.choice_cact = 0
   
    def update(self, game):
        self.choice_cact = random.randint(0,1)
        if len(self.obstacles) == 0:
            if self.choice_cact == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            else:
                self.obstacles.append(Cactus(LARGE_CACTUS))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break

    def draw (self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
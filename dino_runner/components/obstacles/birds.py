import random

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Birds(Obstacle):
    def __init__(self):
        self.type = random.randint(0,1)
        super().__init__(BIRD, self.type)
        self.step_index = 0
        if self.type == 0:
            self.rect.y = 250
        else:
            self.rect.y = 325

    
    def draw(self, screen):
        if self.step_index >= 5:
            screen.blit(self.image[0], self.rect)
        else:
            screen.blit(self.image[1], self.rect)
        self.step_index += 1

        if self.step_index >= 10:
            self.step_index = 0
import random

from dino_runner.utils.constants import SMALL_CACTUS
from dino_runner.utils.constants import LARGE_CACTUS

from dino_runner.components.obstacles.obstacle import Obstacle

class Cactus(Obstacle):
    cactus = {
        1: SMALL_CACTUS,
        2: LARGE_CACTUS
    }
    
    def __init__(self):
        self.choice_cact = random.randint(1,2)
        image = self.cactus[self.choice_cact]
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        if self.choice_cact == 1: 
            self.rect.y = 325
        else: 
            self.rect.y = 300 

import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        
    dic_powers = {1: Shield, 2: Hammer}

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint( 200, 300)
            choice_random = random.randint(1,2)
            self.power_ups.append(self.dic_powers[choice_random]())

    def update(self, game):
        self.generate_power_up(game.score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                if type(power_up) == Shield:
                    game.player.shield = True
                    game.player.hammer = False
                    game.game_speed = game.game_speed - 4
                else:
                    game.player.hammer = True
                    game.player.shield = False
                    
                game.player.has_power_up = True
                game.player.type = power_up.type
                game.player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
    
    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)

import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
FONT_STYLE = "freesansbold.ttf"

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.final_score = 0
        self.death_count = 0
        self.comparator = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        
        pygame.display.quit()
        pygame.quit()
    
    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()    

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.update_score()
        #print(self.game_speed)
        
    def update_score(self):
        self.score += 1
        if self.score % 500 == 0:
            self.game_speed += 3
        
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        self.default_text(f"Score: {self.score}", 850, 15)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.default_text(f'{self.player.type.capitalize()} enable for {time_to_show} seconds.', 500, 40)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
            elif event.type == pygame.KEYDOWN and self.death_count > self.comparator:
                self.final_score = 0
                self.comparator += 1

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            self.default_text("PRESS ANY KEY TO START", half_screen_width - 150, half_screen_height - 150)   
        else:
            self.screen.blit(ICON, (half_screen_width - 10, half_screen_height - 50))
            self.default_text("PRESS A KEY TO PLAY AGAIN", half_screen_width - 150, half_screen_height - 150)
            self.default_text(f"SCORE REACHED: {self.final_score}", half_screen_width - 130, half_screen_height - 110)
            self.default_text(f"DEATHS: {self.death_count} ", half_screen_width - 130, half_screen_height - 70)
            self.game_speed = 20
        
        pygame.display.update()
        self.handle_events_on_menu()
                  
    def default_text(self, text_to_display, half_screen_width , half_screen_height):
            font = pygame.font.Font(FONT_STYLE, 22)
            text = font.render(text_to_display, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect_center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect_center)

import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, GAME_OVER, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, DEAD
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
        self.color_bg = False
        self.color_white = 300
        self.color_black = 150

        self.score = 0
        self.final_score = 0
        self.bonus_score = 0
        self.final_bonus_score = 0
        self.best_score = 0
        self.death_count = 0
        self.comparator = 0
        
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

        pygame.mixer.music.load("dino_runner/assets/Music/fight.wav")
        pygame.mixer.music.play(-1)

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        
        pygame.display.quit()
        pygame.quit()
    
    def run(self):
        # Game loop: events - update - draw
        for i in range(3, 0, -1):
            self.screen.fill((255, 255, 255))
            self.default_text(str(i), 50, (0, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.update()
            pygame.time.delay(1000)
        self.bonus_score = 0
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.dark_mode()
    
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
        print(self.game_speed)
        
    def update_score(self):
        self.score += 1
        if self.score % 500 == 0:
            self.game_speed += 3

    def draw(self):
        self.clock.tick(FPS)
        if  self.color_bg == False:
            self.screen.fill(('#FFFFFF')) #Também aceita código hexadecimal "#FFFFFF"
        elif self.color_bg == True:
            self.screen.fill(('#000000')) #Também aceita código hexadecimal "#FFFFFF"
        
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
        if self.color_bg == True:
            self.default_text(f"Score: {self.score}", 22, (255, 255, 255), 850, 15)
            self.default_text(f"Bonus score: {self.bonus_score}", 22, (255, 255, 255), 850, 50)
        else:
            self.default_text(f"Score: {self.score}", 22, (0, 0, 0), 850, 15)
            self.default_text(f"Bonus score: {self.bonus_score}", 22, (0, 0, 0), 850, 50)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                if self.color_bg == True:
                    self.default_text(f'{self.player.type.capitalize()} enable for {time_to_show} seconds.', 22, (255, 255, 255), 380, 15)
                else:
                    self.default_text(f'{self.player.type.capitalize()} enable for {time_to_show} seconds.', 22, (0, 0, 0), 380, 15)
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
                self.final_bonus_score = 0
                self.comparator += 1

                
    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            self.default_text("PRESS ANY KEY TO START", 24, (0, 0, 0), half_screen_width - 150, half_screen_height - 150)   
        else:
            self.screen.blit(GAME_OVER, (half_screen_width - 210, half_screen_height - 200))
            self.screen.blit(ICON, (half_screen_width - 80, half_screen_height + 80))
            self.default_text(f"-Best score: {self.best_score}", 24, (0, 0, 0), half_screen_width - 130, half_screen_height - 110)
            self.default_text(f"-Score reached: {self.final_score}", 24, (0, 0, 0), half_screen_width - 130, half_screen_height - 80)
            self.default_text(f"-Bonus score: {self.final_bonus_score}", 24, (0, 0, 0), half_screen_width - 130, half_screen_height - 50)
            self.default_text(f"-Deaths: {self.death_count} ", 24, (0, 0, 0), half_screen_width - 130, half_screen_height - 20)
            self.default_text(f"PRESS ANY KEY TO PLAY AGAIN", 24, (0, 0, 0), half_screen_width - 190, half_screen_height + 220)
            self.game_speed = 20
    
        pygame.display.update()
        self.handle_events_on_menu()
                  
    def default_text(self, text_to_display, size_text, color_text, half_screen_width , half_screen_height):
            font = pygame.font.Font(FONT_STYLE, size_text)
            text = font.render(text_to_display, True, color_text)
            text_rect = text.get_rect()
            text_rect_center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect_center)

    

    def dark_mode(self):
        if self.score >= self.color_black:
            self.color_bg = True
            self.color_black *= 4  
        elif self.score >= self.color_white:
                self.color_bg = False
                self.color_white *= 3
                
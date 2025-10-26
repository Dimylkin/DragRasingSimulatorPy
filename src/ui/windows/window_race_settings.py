import sys
import pygame

from src.ui.tools.tool_window_designer import Button
from src.game.game_race_manager import RaceManager
from src.utils.utils_paths import get_asset_path, get_resource_path


class RaceSettings:
    def __init__(self):
        pygame.init()

        self.window_size = (800, 600)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Драг рейсинг")
        self.screen.fill((255, 127, 80))
        self.font = pygame.font.Font(None, 40)
        self.button_off_color = (240, 230, 210)
        self.button_on_color = (255, 245, 225)
        self._load_resources()
        self.race_manager = RaceManager()

        self.is_running = True
        self.clock = pygame.time.Clock()

    def _load_resources(self):
        self.image_track = pygame.image.load(get_resource_path('images', 'tracks', f'track_rainy_swedish_road.jpg')).convert_alpha()
        self.image_car = pygame.image.load(get_resource_path('images','cars', f'car_audi_rs6.png')).convert_alpha()

        self.button_map = Button(self.screen, 290, 80, 200, 100
                            , 2, 15, self.button_on_color
                            , self.button_off_color, None, self.image_track)

        self.button_car = Button(self.screen, 290, 280, 200, 100
                            , 2, 15, self.button_on_color
                            , self.button_off_color, None, self.image_car)

        self.button_mode_bot = Button(self.screen, 200, 480, 200, 100
                                 , 2, 15, self.button_on_color
                                 , self.button_off_color, "Игра с ботом", None)

        self.button_mode_alone = Button(self.screen, 450, 480, 200, 100
                                   , 2, 15, self.button_on_color
                                   , self.button_off_color, "Одиночная игра", None, self.switch_to_race)

        self.text_choice_map = self.font.render("Выберите карту", True, self.button_on_color)
        self.text_choice_car = self.font.render("Выберите машину", True, self.button_on_color)
        self.text_choice_mode = self.font.render("Выберите режим игры", True, self.button_on_color)

    def switch_to_race(self):
        self.is_running = False
        self.race_manager.run()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _draw(self):
        self.screen.blit(self.text_choice_map, (280, 20))
        self.button_map.button_with_image()
        self.screen.blit(self.text_choice_car, (280, 220))
        self.button_car.button_with_image()
        self.screen.blit(self.text_choice_mode, (280, 420))
        self.button_mode_bot.button_with_text()
        self.button_mode_alone.button_with_text()

    def run(self):
        while self.is_running:
            self.screen.fill((255, 127, 80))
            self._handle_events()
            self._draw()

            pygame.display.flip()
            self.clock.tick(60)
        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()
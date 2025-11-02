import pygame
import sys

from src.ui.tools.tool_window_designer import WindowPattern, WindowObject
from src.ui.windows.window_statistic import WindowStatistic
from src.ui.windows.window_race_settings import RaceSettings
from src.ui.windows.window_config_app import WindowSettings


class WindowStart:
    def __init__(self, user):
        pygame.init()
        
        window = WindowPattern()
        self.screen = pygame.display.set_mode(window.get_screen_size())
        pygame.display.set_caption(window.get_screen_caption())
        self.screen_fill = window.get_screen_color()
        self.screen.fill(self.screen_fill)
        
        self.font_middle = window.get_font("middle")
        self.text_simple_color = window.get_text_colors("simple")
        
        self._load_resources()
        
        self.user = user
        self.window_race_settings = None
        self.window_statistic = None
        self.window_settings = None


        self.is_running = True
        self.clock = pygame.time.Clock()

    def _load_resources(self):
        self.text_welcome = self.font_middle.render("Добро пожаловать в Драг Рейсинг!", True, self.text_simple_color)
        text_welcome_rect = self.text_welcome.get_rect(center=(self.screen.get_width() // 2, 150))

        button_width, button_height = 220, 80
        button_margin = 30
        start_x = (self.screen.get_width() - button_width * 2 - button_margin) // 2
        start_y = 230

        self.button_window_race_settings = WindowObject(
            self.screen, start_x, start_y, button_width, button_height,
            15, "Начать игру", None, self.switch_to_window_race_settings
        )

        self.button_window_statistic = WindowObject(
            self.screen, start_x + button_width + button_margin, start_y,
            button_width, button_height, 15, "Статистика", None,
            self.switch_to_window_statistic
        )

        self.button_window_settings = WindowObject(
            self.screen, start_x, start_y + button_height + button_margin,
            button_width, button_height, 15, "Настройки", None,
            self.switch_to_window_settings
        )

        self.button_exit = WindowObject(
            self.screen, start_x + button_width + button_margin,
                         start_y + button_height + button_margin, button_width, button_height,
            15, "Выйти", None, self.switch_to_exit
        )

        self.text_welcome_pos = text_welcome_rect

    def switch_to_window_race_settings(self):
        self.is_running = False
        from src.ui.windows.window_race_settings import RaceSettings
        race_settings = RaceSettings(self.user)
        race_settings.run()

    def switch_to_window_statistic(self):
        self.is_running = False
        from src.ui.windows.window_statistic import WindowStatistic
        statistic = WindowStatistic(self.user)
        statistic.run()

    def switch_to_window_settings(self):
        self.is_running = False
        from src.ui.windows.window_config_app import WindowSettings
        settings = WindowSettings(self.user)
        settings.run()

    def switch_to_exit(self):
        self.is_running = False

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _draw(self):
        self.screen.fill(self.screen_fill)

        self.screen.blit(self.text_welcome, self.text_welcome_pos)

        self.button_window_race_settings.obj_button_with_text()
        self.button_window_statistic.obj_button_with_text()
        self.button_window_settings.obj_button_with_text()
        self.button_exit.obj_button_with_text()

    def run(self):
        while self.is_running:
            self._handle_events()
            self._draw()

            pygame.display.flip()
            self.clock.tick(60)
        self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
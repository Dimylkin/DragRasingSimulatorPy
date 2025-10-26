import pygame

from src.ui.tools.tool_window_designer import Button
from src.ui.windows.window_race_settings import RaceSettings

class Start:
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
        self.race_settings = RaceSettings()

        self.is_running = True
        self.clock = pygame.time.Clock()

    def _load_resources(self):
        self.text_welcome = self.font.render("!Добро пожаловать в игру про Драг Рейсинг!", True, self.button_on_color)
        self.button_start = Button(self.screen, 150, 300, 200, 100
                              , 2, 15, self.button_on_color, self.button_off_color
                              , "Начать игру!", None, self.switch_to_choice)
        self.button_exit = Button(self.screen, 450, 300, 200, 100
                             , 2, 15, self.button_on_color, self.button_off_color
                             , "Выйти из игры :(", None, self.switch_to_exit)

    def switch_to_choice(self):
        print("Переключаемся на окно выбора...")
        self.is_running = False  # Останавливаем текущее окно
        self.race_settings.run()  # Запускаем новое окно

    def switch_to_exit(self):
        self.is_running = False

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _draw(self):
        self.screen.fill((255, 127, 80))
        self.screen.blit(self.text_welcome, (100, 200))
        self.button_start.button_with_text()
        self.button_exit.button_with_text()


    def run(self):
        while self.is_running:
            self._handle_events()
            self._draw()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    start = Start()
    start.run()
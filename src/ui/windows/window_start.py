"""
Модуль стартового окна приложения.

Содержит класс WindowStart для управления главным меню игры,
предоставляющим доступ к началу игры, статистике, настройкам и выходу.
"""

import pygame
import sys

from src.ui.tools.tool_window_designer import WindowPattern, WindowObject


class WindowStart:
    """
    Класс стартового окна игры.

    Предоставляет главное меню с кнопками для навигации по различным
    разделам игры: начало игры, статистика, настройки и выход.

    Attributes:
        user: Объект текущего пользователя.
        screen (pygame.Surface): Поверхность экрана для отрисовки.
        is_running (bool): Флаг работы окна.
    """

    def __init__(self, user):
        """
        Инициализирует стартовое окно.

        Args:
            user: Объект пользователя.
        """
        pygame.init()

        self.user = user

        window = WindowPattern()
        self.screen = pygame.display.set_mode(window.get_screen_size())
        pygame.display.set_caption(window.get_screen_caption())
        self.screen_fill = window.get_screen_color()
        self.screen.fill(self.screen_fill)

        self.font_middle = window.get_font("medium")
        self.text_simple_color = window.get_text_colors("simple")

        self._load_resources()

        self.is_running = True
        self.clock = pygame.time.Clock()

    def _load_resources(self):
        """
        Загружает ресурсы и создает UI-элементы стартового окна.

        Создает приветственный текст и кнопки для навигации по меню:
        начало игры, статистика, настройки и выход.
        """
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
        """
        Переключает на окно настроек гонки.

        Закрывает стартовое окно и открывает окно выбора автомобиля и трека.
        """
        self.is_running = False
        from src.ui.windows.window_race_settings import RaceSettings
        race_settings = RaceSettings(self.user)
        race_settings.run()

    def switch_to_window_statistic(self):
        """
        Переключает на окно статистики.

        Закрывает стартовое окно и открывает окно со статистикой игрока.
        """
        self.is_running = False
        from src.ui.windows.window_statistic import WindowStatistic
        statistic = WindowStatistic(self.user)
        statistic.run()

    def switch_to_window_settings(self):
        """
        Переключает на окно настроек приложения.

        Закрывает стартовое окно и открывает окно настроек UI.
        """
        self.is_running = False
        from src.ui.windows.window_config_app import WindowSettings
        settings = WindowSettings(self.user)
        settings.run()

    def switch_to_exit(self):
        """
        Завершает работу приложения.

        Устанавливает флаг завершения работы главного цикла.
        """
        self.is_running = False

    def _handle_events(self):
        """
        Обрабатывает события Pygame.

        Обрабатывает события закрытия окна.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _draw(self):
        """
        Отрисовывает все элементы стартового окна.

        Рисует фон, приветственный текст и все кнопки меню.
        """
        self.screen.fill(self.screen_fill)

        self.screen.blit(self.text_welcome, self.text_welcome_pos)

        self.button_window_race_settings.obj_button_with_text()
        self.button_window_statistic.obj_button_with_text()
        self.button_window_settings.obj_button_with_text()
        self.button_exit.obj_button_with_text()

    def run(self):
        """
        Запускает главный цикл стартового окна.

        Обрабатывает события и отрисовывает UI с частотой 60 кадров
        в секунду до закрытия окна.
        """
        while self.is_running:
            self._handle_events()
            self._draw()

            pygame.display.flip()
            self.clock.tick(60)
        self.quit()

    @staticmethod
    def quit():
        """
        Завершает работу Pygame и выходит из программы.
        """
        pygame.quit()
        sys.exit()

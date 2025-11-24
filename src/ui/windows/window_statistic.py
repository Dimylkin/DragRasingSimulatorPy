"""
Модуль окна статистики игрока.

Содержит класс WindowStatistic для отображения информации о пользователе,
включая аватар, имя и текущее количество очков.
"""

import pygame
import sys

from src.ui.tools.tool_window_designer import WindowObject, WindowPattern
from src.utils.utils_paths import Utils


class WindowStatistic:
    """
    Класс окна статистики игрока.

    Отображает профиль пользователя с аватаром, именем и счетом.
    Предоставляет навигацию для возврата в главное меню.

    Attributes:
        user: Объект текущего пользователя.
        screen (pygame.Surface): Поверхность экрана для отрисовки.
        is_running (bool): Флаг работы окна.
    """

    def __init__(self, user):
        """
        Инициализирует окно статистики.

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

        self.font_large = window.get_font("large")
        self.text_simple_color = window.get_text_colors("simple")

        self._load_resource()

        self.is_running = True
        self.clock = pygame.time.Clock()

    def _load_resource(self):
        """
        Загружает ресурсы и создает UI-элементы окна статистики.

        Загружает аватар пользователя, создает текстовые элементы
        с информацией о пользователе и кнопку возврата.

        Raises:
            FileNotFoundError: Если изображение пользователя не найдено.
            pygame.error: Если возникла ошибка загрузки изображения.
        """
        try:
            self.user_image = pygame.image.load(
                Utils().get_resource_path('images', 'users', self.user.image)
            ).convert_alpha()
        except (FileNotFoundError, pygame.error) as e:
            print(f"Ошибка загрузки аватара пользователя: {e}")
            self.user_image = pygame.Surface((200, 200))
            self.user_image.fill((128, 128, 128))

        self.text_title = self.font_large.render("Статистика игрока", True, self.text_simple_color)

        self.user_avatar = WindowObject(self.screen, 50, 80, 200, 200,
                                        100, None, self.user_image)

        self.text_user_name = self.font_large.render(f"Имя: {self.user.nickname}", True, self.text_simple_color)

        self.text_user_score = self.font_large.render(f"Очки: {self.user.score}", True,
                                                      self.text_simple_color)

        self.text_user_statistics = self.font_large.render("Статистика лучших рейсов:", True,
                                                      self.text_simple_color)

        self.button_back = WindowObject(self.screen, 30, 20, 75, 30,
                                        5, "Назад", None, self.window_back)

    def window_back(self):
        """
        Возвращает пользователя в стартовое окно.

        Закрывает текущее окно статистики и открывает главное меню.
        """
        from src.ui.windows.window_start import WindowStart
        start = WindowStart(self.user)
        self.is_running = False
        start.run()

    def draw(self):
        self.screen.fill(self.screen_fill)

        self.button_back.obj_button_with_text()
        self.user_avatar.obj_image()

        rect_title = self.text_title.get_rect(center=(400, 40))
        self.screen.blit(self.text_title, rect_title)

        rect_name = self.text_user_name.get_rect(center=(500, 125))
        self.screen.blit(self.text_user_name, rect_name)

        rect_score = self.text_user_score.get_rect(center=(500, 200))
        self.screen.blit(self.text_user_score, rect_score)

        rect_statistics = self.text_user_statistics.get_rect(center=(400, 310))
        self.screen.blit(self.text_user_statistics, rect_statistics)

        font_small = WindowPattern().get_font("small")
        color = self.text_simple_color

        x_pos = 25 + 750 // 2
        y_start = 340 + 30
        line_height = 40

        if len(self.user.data) != 0:
            for i, (car_name, stats) in enumerate(self.user.data.items()):
                best_time = stats.get('best_time')

                time_str = f"{best_time:.2f} сек" if best_time is not None else "-"

                text_line = f"Машина: {car_name}: Время: {time_str}"
                text_surface = font_small.render(text_line, True, color)
                rect_text = text_surface.get_rect(center=(x_pos, y_start + i * line_height))
                self.screen.blit(text_surface, rect_text)
        else:
            text_surface = self.font_large.render("Здесь пока пусто!", True, color)
            self.screen.blit(text_surface, (250, y_start + line_height))

    def _handle_events(self):
        """
        Обрабатывает события Pygame.

        Обрабатывает события закрытия окна.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def run(self):
        """
        Запускает главный цикл окна статистики.

        Обрабатывает события и отрисовывает UI с частотой 60 кадров
        в секунду до закрытия окна.
        """
        while self.is_running:
            self._handle_events()
            self.user._load_resources(self.user.name)
            self.draw()

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
"""
Модуль окна настроек приложения.

Содержит класс WindowSettings для управления интерфейсом настроек,
позволяющим пользователю изменять размер окна, цветовую схему и другие параметры UI.
"""

import pygame
import sys
import json

from src.ui.tools.tool_window_designer import WindowObject, WindowPattern, InputBox
from src.utils.utils_paths import Utils


class WindowSettings:
    """
    Класс окна настроек приложения.

    Предоставляет интерфейс для изменения размера окна, цветов фона,
    текста, успеха и ошибок. Позволяет применять, сохранять и сбрасывать
    настройки к значениям по умолчанию.

    Attributes:
        screen (pygame.Surface): Поверхность экрана для отрисовки.
        user: Объект текущего пользователя.
        is_running (bool): Флаг работы окна.
        message_text (str): Текст сообщения для отображения.
        message_timer (int): Таймер отображения сообщения в кадрах.
        message_success (bool): Флаг успешности операции для выбора цвета сообщения.
    """

    def __init__(self, user):
        """
        Инициализирует окно настроек.

        Args:
            user: Объект пользователя.
        """
        pygame.init()

        window = WindowPattern()

        self.screen = pygame.display.set_mode(window.get_screen_size())
        pygame.display.set_caption(window.screen_caption)
        self.screen_fill = window.get_screen_color()
        self.screen.fill(self.screen_fill)

        self.font_large = window.get_font("large")
        self.font_medium = window.get_font("medium")
        self.font_small = window.get_font("small")

        self.text_simple_color = window.get_text_colors("simple")
        self.text_success_color = window.get_text_colors("success")
        self.text_error_color = window.get_text_colors("unsuccess")

        self.user = user
        self._load_resources()

        self.is_running = True
        self.clock = pygame.time.Clock()

    def _load_resources(self):
        """
        Загружает ресурсы и создает UI-элементы окна настроек.

        Создает все поля ввода, кнопки и текстовые метки,
        заполняя их текущими значениями из конфигурационных файлов.
        """

        app_settings = self._load_app_settings()
        text_settings = self._load_text_settings()

        width = app_settings.get('width', 800)
        height = app_settings.get('height', 600)
        bg_color = app_settings.get('color', [255, 127, 80])

        text_color = text_settings.get('simple_color', [255, 245, 225])
        success_color = text_settings.get('success_color', [152, 251, 152])
        error_color = text_settings.get('unsuccess_color', [123, 0, 28])

        self.button_back = WindowObject(self.screen, 30, 20, 75, 30,
                                        5, "Назад", None, self.window_back)

        self.text_title = self.font_large.render("Настройки приложения", True, self.text_simple_color)

        label_x = 100
        input_x = 350

        self.text_window_size = self.font_medium.render("Размер окна:", True, self.text_simple_color)
        self.input_width = InputBox(input_x, 100, 80, 32, str(width), True, False)
        self.input_height = InputBox(input_x + 130, 100, 80, 32, str(height), True, False)
        self.text_x = self.font_small.render("x", True, self.text_simple_color)

        self.text_bg_color = self.font_medium.render("Цвет фона (RGB):", True, self.text_simple_color)
        self.input_bg_r = InputBox(input_x, 150, 60, 32, str(bg_color[0]), True,
                                   True)
        self.input_bg_g = InputBox(input_x + 70, 150, 60, 32, str(bg_color[1]), True, True)
        self.input_bg_b = InputBox(input_x + 140, 150, 60, 32, str(bg_color[2]), True, True)

        self.text_normal_color = self.font_medium.render("Цвет текста (RGB):", True, self.text_simple_color)
        self.input_text_r = InputBox(input_x, 200, 60, 32, str(text_color[0]), True,
                                     True)
        self.input_text_g = InputBox(input_x + 70, 200, 60, 32, str(text_color[1]), True, True)
        self.input_text_b = InputBox(input_x + 140, 200, 60, 32, str(text_color[2]), True, True)

        self.text_success_color_label = self.font_medium.render("Цвет успеха (RGB):", True, self.text_simple_color)
        self.input_success_r = InputBox(input_x, 250, 60, 32, str(success_color[0]), True,
                                        True)
        self.input_success_g = InputBox(input_x + 70, 250, 60, 32, str(success_color[1]), True, True)
        self.input_success_b = InputBox(input_x + 140, 250, 60, 32, str(success_color[2]), True, True)

        self.text_error_color_label = self.font_medium.render("Цвет ошибки (RGB):", True, self.text_simple_color)
        self.input_error_r = InputBox(input_x, 300, 60, 32, str(error_color[0]), True,
                                      True)
        self.input_error_g = InputBox(input_x + 70, 300, 60, 32, str(error_color[1]), True, True)
        self.input_error_b = InputBox(input_x + 140, 300, 60, 32, str(error_color[2]), True, True)

        self.button_apply = WindowObject(self.screen, 250, 350, 150, 40,
                                         10, "Применить", None, self.apply_settings)
        self.button_reset = WindowObject(self.screen, 420, 350, 150, 40,
                                         10, "Сбросить", None, self.reset_settings)

        self.message_text = ""
        self.message_timer = 0
        self.message_success = False

        self.label_x = label_x
        self.input_x = input_x

    def _load_app_settings(self):
        """
        Загружает настройки приложения из файла конфигурации.

        Returns:
            dict: Словарь с настройками приложения (width, height, color).
                  При ошибке возвращает значения по умолчанию.
        """
        try:
            with open(Utils().get_asset_path('config_ui', 'config_ui_app.json'), 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка загрузки настроек приложения: {e}")
            return {
                'width': 800,
                'height': 600,
                'color': [255, 127, 80]
            }

    def _load_text_settings(self):
        """
        Загружает настройки цветов текста из файла конфигурации.

        Returns:
            dict: Словарь с цветами текста (simple_color, success_color, unsuccess_color).
                  При ошибке возвращает значения по умолчанию.
        """
        try:
            with open(Utils().get_asset_path('config_ui', 'config_ui_text.json'), 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка загрузки настроек текста: {e}")
            return {
                'simple_color': [255, 245, 225],
                'success_color': [152, 251, 152],
                'unsuccess_color': [123, 0, 28]
            }

    def window_back(self):
        """
        Возвращает пользователя в стартовое окно.

        Закрывает текущее окно настроек и открывает стартовое окно.
        """
        from src.ui.windows.window_start import WindowStart
        start = WindowStart(self.user)
        self.is_running = False
        start.run()

    def _validate_rgb_value(self, value):
        """
        Валидирует значение RGB компонента.

        Args:
            value: Значение для валидации.

        Returns:
            int: Валидное значение в диапазоне 0-255, или None если невалидно.
        """
        if value is None:
            return None
        try:
            val = int(value)
            if 0 <= val <= 255:
                return val
            return None
        except (ValueError, TypeError):
            return None

    def apply_settings(self):
        """
        Применяет и сохраняет настройки в конфигурационные файлы.

        Валидирует введенные значения размеров окна и RGB-компонентов цветов,
        сохраняет их в JSON-файлы и отображает сообщение о результате.
        """
        try:
            width = self.input_width.get_value()
            height = self.input_height.get_value()

            if width is None or height is None or width < 400 or height < 300:
                self.show_message("Неверный размер окна! (мин. 400x300)", False)
                return

            bg_r = self._validate_rgb_value(self.input_bg_r.get_value())
            bg_g = self._validate_rgb_value(self.input_bg_g.get_value())
            bg_b = self._validate_rgb_value(self.input_bg_b.get_value())

            if None in [bg_r, bg_g, bg_b]:
                self.show_message("Неверные значения цвета фона!", False)
                return

            text_r = self._validate_rgb_value(self.input_text_r.get_value())
            text_g = self._validate_rgb_value(self.input_text_g.get_value())
            text_b = self._validate_rgb_value(self.input_text_b.get_value())

            if None in [text_r, text_g, text_b]:
                self.show_message("Неверные значения цвета текста!", False)
                return

            success_r = self._validate_rgb_value(self.input_success_r.get_value())
            success_g = self._validate_rgb_value(self.input_success_g.get_value())
            success_b = self._validate_rgb_value(self.input_success_b.get_value())

            if None in [success_r, success_g, success_b]:
                self.show_message("Неверные значения цвета успеха!", False)
                return

            error_r = self._validate_rgb_value(self.input_error_r.get_value())
            error_g = self._validate_rgb_value(self.input_error_g.get_value())
            error_b = self._validate_rgb_value(self.input_error_b.get_value())

            if None in [error_r, error_g, error_b]:
                self.show_message("Неверные значения цвета ошибки!", False)
                return

            bg_color = [bg_r, bg_g, bg_b]
            text_color = [text_r, text_g, text_b]
            success_color = [success_r, success_g, success_b]
            error_color = [error_r, error_g, error_b]

            with open(Utils().get_asset_path('config_ui', 'config_ui_app.json'), 'w', encoding='utf-8') as file:
                json.dump({
                    'width': width,
                    'height': height,
                    'color': bg_color
                }, file, indent=2, ensure_ascii=False)

            with open(Utils().get_asset_path('config_ui', 'config_ui_text.json'), 'w', encoding='utf-8') as file:
                json.dump({
                    'simple_color': text_color,
                    'success_color': success_color,
                    'unsuccess_color': error_color
                }, file, indent=2, ensure_ascii=False)

            WindowPattern._initialized = False
            WindowPattern._instance = None

            self.show_message("Настройки применены! Перезапустите приложение.", True)

        except (ValueError, TypeError, IOError) as e:
            print(f"Ошибка применения настроек: {e}")
            self.show_message("Ошибка в данных!", False)

    def reset_settings(self):
        """
        Сбрасывает настройки к значениям по умолчанию.

        Устанавливает все поля в значения по умолчанию,
        сохраняет их в файлы и отображает сообщение.
        """
        try:
            defaults = {
                'width': 800,
                'height': 600,
                'bg_color': [255, 127, 80],
                'text_color': [255, 245, 225],
                'success_color': [152, 251, 152],
                'error_color': [123, 0, 28]
            }

            self.input_width.text = str(defaults['width'])
            self.input_height.text = str(defaults['height'])

            colors = [
                (self.input_bg_r, self.input_bg_g, self.input_bg_b, defaults['bg_color']),
                (self.input_text_r, self.input_text_g, self.input_text_b, defaults['text_color']),
                (self.input_success_r, self.input_success_g, self.input_success_b, defaults['success_color']),
                (self.input_error_r, self.input_error_g, self.input_error_b, defaults['error_color'])
            ]

            for r_input, g_input, b_input, color in colors:
                r_input.text = str(color[0])
                g_input.text = str(color[1])
                b_input.text = str(color[2])

            with open(Utils().get_asset_path('config_ui', 'config_ui_app.json'), 'w', encoding='utf-8') as file:
                json.dump({
                    'width': defaults['width'],
                    'height': defaults['height'],
                    'color': defaults['bg_color']
                }, file, indent=2, ensure_ascii=False)

            with open(Utils().get_asset_path('config_ui', 'config_ui_text.json'), 'w', encoding='utf-8') as file:
                json.dump({
                    'simple_color': defaults['text_color'],
                    'success_color': defaults['success_color'],
                    'unsuccess_color': defaults['error_color']
                }, file, indent=2, ensure_ascii=False)

            WindowPattern._initialized = False
            WindowPattern._instance = None

            self.show_message("Настройки сброшены! Перезапустите приложение.", True)

        except IOError as e:
            print(f"Ошибка сброса настроек: {e}")
            self.show_message("Ошибка записи в файлы!", False)

    def show_message(self, text, success):
        """
        Отображает временное сообщение на экране.

        Args:
            text (str): Текст сообщения.
            success (bool): True для успешного сообщения (зеленый),
                           False для сообщения об ошибке (красный).
        """
        self.message_text = text
        self.message_timer = 180
        self.message_success = success

    def _handle_events(self):
        """
        Обрабатывает события Pygame.

        Обрабатывает события закрытия окна и передает события
        всем полям ввода для обработки ввода с клавиатуры и мыши.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            input_boxes = [
                self.input_width, self.input_height,
                self.input_bg_r, self.input_bg_g, self.input_bg_b,
                self.input_text_r, self.input_text_g, self.input_text_b,
                self.input_success_r, self.input_success_g, self.input_success_b,
                self.input_error_r, self.input_error_g, self.input_error_b
            ]

            for input_box in input_boxes:
                input_box.handle_event(event)

    def draw(self):
        """
        Отрисовывает все элементы окна настроек.

        Рисует фон, заголовок, все текстовые метки, поля ввода,
        кнопки и временное сообщение (если активно).
        """
        self.screen.fill(self.screen_fill)

        title_rect = self.text_title.get_rect(center=(400, 50))
        self.screen.blit(self.text_title, title_rect)

        self.button_back.obj_button_with_text()

        self.screen.blit(self.text_window_size, (50, 100))
        self.input_width.draw(self.screen)
        self.screen.blit(self.text_x, (450, 105))
        self.input_height.draw(self.screen)

        self.screen.blit(self.text_bg_color, (50, 150))
        self.input_bg_r.draw(self.screen)
        self.input_bg_g.draw(self.screen)
        self.input_bg_b.draw(self.screen)

        self.screen.blit(self.text_normal_color, (50, 200))
        self.input_text_r.draw(self.screen)
        self.input_text_g.draw(self.screen)
        self.input_text_b.draw(self.screen)

        self.screen.blit(self.text_success_color_label, (50, 250))
        self.input_success_r.draw(self.screen)
        self.input_success_g.draw(self.screen)
        self.input_success_b.draw(self.screen)

        self.screen.blit(self.text_error_color_label, (50, 300))
        self.input_error_r.draw(self.screen)
        self.input_error_g.draw(self.screen)
        self.input_error_b.draw(self.screen)

        self.button_apply.obj_button_with_text()
        self.button_reset.obj_button_with_text()

        if self.message_timer > 0:
            color = self.text_success_color if self.message_success else self.text_error_color
            message_surface = self.font_small.render(self.message_text, True, color)
            message_rect = message_surface.get_rect(center=(400, 420))
            self.screen.blit(message_surface, message_rect)
            self.message_timer -= 1

    def run(self):
        """
        Запускает главный цикл окна настроек.

        Обрабатывает события, отрисовывает UI и обновляет экран
        с частотой 60 кадров в секунду до закрытия окна.
        """
        while self.is_running:
            self._handle_events()
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

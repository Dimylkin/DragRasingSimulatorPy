import pygame
import sys
import json

from src.ui.tools.tool_window_designer import WindowObject, WindowPattern, InputBox
from src.utils.utils_paths import Utils


class WindowSettings:
    def __init__(self, user):
        pygame.init()

        window = WindowPattern()

        self.screen = pygame.display.set_mode(window.get_screen_size())
        pygame.display.set_caption(window.screen_caption)
        self.screen_fill = window.get_screen_color()
        self.screen.fill(self.screen_fill)

        self.font_large = window.get_font("large")
        self.font_medium = window.get_font("middle")
        self.font_small = window.get_font("small")

        self.text_simple_color = window.get_text_colors("simple")
        self.text_success_color = window.get_text_colors("success")
        self.text_error_color = window.get_text_colors("error")

        self.user = user
        self._load_resources()

        self.is_running = True
        self.clock = pygame.time.Clock()

    def _load_resources(self):
        # Загружаем текущие настройки из файлов
        app_settings = self._load_app_settings()
        text_settings = self._load_text_settings()

        # Извлекаем значения или используем значения по умолчанию
        width = app_settings.get('width', 800)
        height = app_settings.get('height', 600)
        bg_color = app_settings.get('color', [255, 127, 80])  # Уже список чисел

        text_color = text_settings.get('simple_color', [255, 245, 225])  # Уже список чисел
        success_color = text_settings.get('success_color', [152, 251, 152])  # Уже список чисел
        error_color = text_settings.get('unsuccess_color', [123, 0, 28])  # Уже список чисел

        self.button_back = WindowObject(self.screen, 30, 20, 75, 30,
                                        5, "Назад", None, self.window_back)

        self.text_title = self.font_large.render("Настройки приложения", True, self.text_simple_color)

        label_x = 100
        input_x = 350

        # Заполняем поля текущими значениями
        self.text_window_size = self.font_medium.render("Размер окна:", True, self.text_simple_color)
        self.input_width = InputBox(input_x, 100, 80, 32, str(width), True)
        self.input_height = InputBox(input_x + 130, 100, 80, 32, str(height), True)
        self.text_x = self.font_small.render("x", True, self.text_simple_color)

        self.text_bg_color = self.font_medium.render("Цвет фона (RGB):", True, self.text_simple_color)
        self.input_bg_r = InputBox(input_x, 150, 60, 32, str(bg_color[0]), True)
        self.input_bg_g = InputBox(input_x + 70, 150, 60, 32, str(bg_color[1]), True)
        self.input_bg_b = InputBox(input_x + 140, 150, 60, 32, str(bg_color[2]), True)

        self.text_normal_color = self.font_medium.render("Цвет текста (RGB):", True, self.text_simple_color)
        self.input_text_r = InputBox(input_x, 200, 60, 32, str(text_color[0]), True)
        self.input_text_g = InputBox(input_x + 70, 200, 60, 32, str(text_color[1]), True)
        self.input_text_b = InputBox(input_x + 140, 200, 60, 32, str(text_color[2]), True)

        self.text_success_color_label = self.font_medium.render("Цвет успеха (RGB):", True, self.text_simple_color)
        self.input_success_r = InputBox(input_x, 250, 60, 32, str(success_color[0]), True)
        self.input_success_g = InputBox(input_x + 70, 250, 60, 32, str(success_color[1]), True)
        self.input_success_b = InputBox(input_x + 140, 250, 60, 32, str(success_color[2]), True)

        self.text_error_color_label = self.font_medium.render("Цвет ошибки (RGB):", True, self.text_simple_color)
        self.input_error_r = InputBox(input_x, 300, 60, 32, str(error_color[0]), True)
        self.input_error_g = InputBox(input_x + 70, 300, 60, 32, str(error_color[1]), True)
        self.input_error_b = InputBox(input_x + 140, 300, 60, 32, str(error_color[2]), True)

        self.button_apply = WindowObject(self.screen, 250, 350, 150, 40,
                                         10, "Применить", None, self.apply_settings)
        self.button_reset = WindowObject(self.screen, 420, 350, 150, 40,
                                         10, "Сбросить", None, self.reset_settings)

        self.message_text = ""
        self.message_timer = 0

        self.label_x = label_x
        self.input_x = input_x

    def _load_app_settings(self):
        """Загружает настройки приложения из файла"""
        try:
            with open(Utils().get_asset_path('config_ui', 'config_ui_app.json'), 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'width': 800,
                'height': 600,
                'color': '(255, 127, 80)'
            }

    def _load_text_settings(self):
        """Загружает настройки текста из файла"""
        try:
            with open(Utils().get_asset_path('config_ui', 'config_ui_text.json'), 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'simple_color': '(255, 245, 225)',
                'success_color': '(152, 251, 152)',
                'unsuccess_color': '(123, 0, 28)'
            }

    def window_back(self):
        from src.ui.windows.window_start import WindowStart
        start = WindowStart(self.user)
        self.is_running = False
        start.run()

    def apply_settings(self):
        try:
            width = self.input_width.get_value() or 800
            height = self.input_height.get_value() or 600

            # Теперь сохраняем цвета как списки чисел
            bg_color = [
                self.input_bg_r.get_value() or 255,
                self.input_bg_g.get_value() or 127,
                self.input_bg_b.get_value() or 80
            ]
            text_color = [
                self.input_text_r.get_value() or 255,
                self.input_text_g.get_value() or 245,
                self.input_text_b.get_value() or 225
            ]
            success_color = [
                self.input_success_r.get_value() or 152,
                self.input_success_g.get_value() or 251,
                self.input_success_b.get_value() or 152
            ]
            error_color = [
                self.input_error_r.get_value() or 123,
                self.input_error_g.get_value() or 0,
                self.input_error_b.get_value() or 28
            ]

            # Сохраняем в файлы (цвета как списки чисел)
            with open(Utils().get_asset_path('config_ui', 'config_ui_app.json'), 'w', encoding='utf-8') as file:
                json.dump({
                    'width': width,
                    'height': height,
                    'color': bg_color  # Список чисел, а не строка
                }, file, indent=2, ensure_ascii=False)

            with open(Utils().get_asset_path('config_ui', 'config_ui_text.json'), 'w', encoding='utf-8') as file:
                json.dump({
                    'simple_color': text_color,  # Список чисел
                    'success_color': success_color,  # Список чисел
                    'unsuccess_color': error_color  # Список чисел
                }, file, indent=2, ensure_ascii=False)

            self.show_message("Настройки применены!", True)


        except (ValueError, TypeError):
            self.show_message("Ошибка в данных!", False)

    def reset_settings(self):
        # Настройки по умолчанию в ЧИСЛОВОМ формате
        defaults = {
            'width': 800,
            'height': 600,
            'bg_color': [255, 127, 80],  # Список чисел
            'text_color': [255, 245, 225],  # Список чисел
            'success_color': [152, 251, 152],  # Список чисел
            'error_color': [123, 0, 28]  # Список чисел
        }

        # Размер окна
        self.input_width.text = str(defaults['width'])
        self.input_height.text = str(defaults['height'])

        # Цвета (уже в числовом формате)
        colors = [
            (self.input_bg_r, self.input_bg_g, self.input_bg_b, defaults['bg_color']),
            (self.input_text_r, self.input_text_g, self.input_text_b, defaults['text_color']),
            (self.input_success_r, self.input_success_g, self.input_success_b, defaults['success_color']),
            (self.input_error_r, self.input_error_g, self.input_error_b, defaults['error_color'])
        ]

        for r_input, g_input, b_input, color in colors:
            r_input.text = str(color[0])  # Теперь color - это список чисел
            g_input.text = str(color[1])
            b_input.text = str(color[2])

        # Сохраняем в файлы в ЧИСЛОВОМ формате
        with open(Utils().get_asset_path('config_ui', 'config_ui_app.json'), 'w', encoding='utf-8') as file:
            json.dump({
                'width': defaults['width'],
                'height': defaults['height'],
                'color': defaults['bg_color']  # Список чисел, не строка
            }, file, indent=2, ensure_ascii=False)

        with open(Utils().get_asset_path('config_ui', 'config_ui_text.json'), 'w', encoding='utf-8') as file:
            json.dump({
                'simple_color': defaults['text_color'],  # Список чисел
                'success_color': defaults['success_color'],  # Список чисел
                'unsuccess_color': defaults['error_color']  # Список чисел
            }, file, indent=2, ensure_ascii=False)

        self.show_message("Настройки сброшены!", True)

    def show_message(self, text, success):
        self.message_text = text
        self.message_timer = 180
        self.message_success = success

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            self.input_width.handle_event(event)
            self.input_height.handle_event(event)
            self.input_bg_r.handle_event(event)
            self.input_bg_g.handle_event(event)
            self.input_bg_b.handle_event(event)
            self.input_text_r.handle_event(event)
            self.input_text_g.handle_event(event)
            self.input_text_b.handle_event(event)
            self.input_success_r.handle_event(event)
            self.input_success_g.handle_event(event)
            self.input_success_b.handle_event(event)
            self.input_error_r.handle_event(event)
            self.input_error_g.handle_event(event)
            self.input_error_b.handle_event(event)

    def draw(self):
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
        while self.is_running:
            self._handle_events()
            self.draw()

            pygame.display.flip()
            self.clock.tick(60)
        self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

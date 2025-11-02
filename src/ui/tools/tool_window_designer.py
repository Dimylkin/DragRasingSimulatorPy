import json
import pygame

from src.utils.utils_paths import Utils

class WindowPattern:
    def __init__(self):
        self.load_resources()
        self.screen_caption = "Драг Рейсинг"

        self.button_enabled_color = self.text_simple_color
        self.button_disabled_color = (240, 230, 210)

        self.text_small_size = pygame.font.Font(None, 30)
        self.text_middle_size = pygame.font.Font(None, 40)
        self.text_large_size = pygame.font.Font(None, 50)

    def load_resources(self):
        with open(Utils().get_asset_path('config_ui', 'config_ui_app.json'), 'r', encoding='utf-8') as file_app:
            data = json.load(file_app)
            self.screen_width = data['width']
            self.screen_height = data['height']
            color_data = data['color']
            self.screen_color = tuple(color_data)

        with open(Utils().get_asset_path('config_ui', 'config_ui_text.json'), 'r', encoding='utf-8') as file_text:
            data = json.load(file_text)

            self.text_simple_color = tuple(data['simple_color'])
            self.text_successful_color = tuple(data['success_color'])
            self.text_unsuccessful_color = tuple(data['unsuccess_color'])

    def get_screen_size(self):
        return self.screen_width, self.screen_height

    def get_screen_color(self):
        return self.screen_color

    def get_screen_caption(self):
        return self.screen_caption

    def get_button_colors(self):
        return self.button_enabled_color, self.button_disabled_color

    def get_text_colors(self, color = 'simple'):
        colors = {
            'simple': self.text_simple_color,
            'success': self.text_successful_color,
            'unsuccess': self.text_unsuccessful_color
        }
        return colors.get(color, self.text_simple_color)

    def get_font(self, size='medium'):
        fonts = {
            'small': self.text_small_size,
            'medium': self.text_middle_size,
            'large': self.text_large_size
        }
        return fonts.get(size, self.text_middle_size)


class WindowObject:
    def __init__(self, screen, coordinate_x, coordinate_y, surface_width, surface_height,
                 radius, text = None, image = None, action = None):
        self.screen = screen
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.surface_width = surface_width
        self.surface_height = surface_height
        self.surface_width_stroke = 2
        self.radius = radius
        self.button_on_color = WindowPattern().button_enabled_color
        self.button_off_color = WindowPattern().button_disabled_color
        self.text = text
        self.font = WindowPattern().get_font("small")
        self.image = image
        self.clicked = False
        self.action = action

    def set_image(self, new_image):
        self.image = new_image

    def obj_image(self):
        surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, self.surface_width, self.surface_height)
        pygame.draw.rect(surface, self.button_on_color, rect, border_radius = self.radius)

        mask = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), rect, border_radius = self.radius)

        scaled_image = pygame.transform.scale(self.image, (self.surface_width, self.surface_height))
        rounded_image = scaled_image.copy()
        rounded_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        surface.blit(rounded_image, (0, 0))

        pygame.draw.rect(surface, (0, 0, 0), rect, self.surface_width_stroke, border_radius = self.radius)
        self.screen.blit(surface, (self.coordinate_x, self.coordinate_y))


    def obj_button_with_text(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, self.surface_width, self.surface_height)
        screen_rect = pygame.Rect(self.coordinate_x, self.coordinate_y, self.surface_width, self.surface_height)
        on_button = screen_rect.collidepoint(mouse)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.surface_width // 2, self.surface_height // 2))

        if on_button:
            pygame.draw.rect(button_surface, self.button_on_color, rect, border_radius=self.radius)

            if click[0] == 1 and not self.clicked:
                self.clicked = True
                if self.action:
                    self.action()
        else:
            pygame.draw.rect(button_surface, self.button_off_color, rect, border_radius=self.radius)
            self.clicked = False

        button_surface.blit(text_surface, text_rect)
        pygame.draw.rect(button_surface, (0, 0, 0), rect, self.surface_width_stroke, border_radius=self.radius)
        self.screen.blit(button_surface, (self.coordinate_x, self.coordinate_y))
        
class InputBox:
    def __init__(self, x, y, w, h, text='', numbers_only=False, is_rgb = False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WindowPattern().get_text_colors("simple")
        self.text = text
        self.txt_surface = WindowPattern().get_font("small").render(text, True, self.color)
        self.active = False
        self.numbers_only = numbers_only
        self.is_rgb = is_rgb
        self.is_valid = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = WindowPattern().get_text_colors("success") if self.active else WindowPattern().get_text_colors("simple")

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Проверяем, что вводится число
                    if self.numbers_only:
                        # Разрешаем только цифры, точку и минус
                        if event.unicode.isdigit():
                            if self.is_rgb == True:
                                if len(self.text) < 3:
                                    self.text += event.unicode
                                    self.is_valid = True
                            else:
                                if len(self.text) < 4:
                                    self.text += event.unicode
                                    self.is_valid = True
                        else:
                            self.is_valid = False
                    else:
                        # Разрешаем любой ввод
                        self.text += event.unicode
                        self.is_valid = True

                # Перерисовываем текст
                self.txt_surface = WindowPattern().get_font("small").render(self.text, True,
                                               WindowPattern().get_text_colors("simple") if not self.is_valid else self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Рисуем текст
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Рисуем рамку (красная если невалидный ввод)
        border_color = WindowPattern().get_text_colors("simple") if not self.is_valid else self.color
        pygame.draw.rect(screen, border_color, self.rect, 2)

    def get_value(self):
        """Возвращает числовое значение, если это возможно"""
        if self.numbers_only and self.text:
            try:
                if '.' in self.text:
                    return float(self.text)
                else:
                    return int(self.text)
            except ValueError:
                return None
        return self.text
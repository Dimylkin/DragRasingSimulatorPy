"""
Модуль для создания UI-элементов в Pygame.

Содержит классы для управления паттернами окон, объектами UI
(кнопки, изображения) и полями ввода текста.
"""

import json
import pygame

from src.utils.utils_paths import Utils


class WindowPattern:
    """
    Класс для управления общими настройками UI приложения.

    Загружает и хранит настройки окна, цветовые схемы, шрифты
    и другие параметры интерфейса из конфигурационных файлов.

    Attributes:
        screen_width (int): Ширина окна приложения.
        screen_height (int): Высота окна приложения.
        screen_color (tuple): RGB цвет фона окна.
        screen_caption (str): Заголовок окна.
        text_simple_color (tuple): RGB цвет обычного текста.
        text_successful_color (tuple): RGB цвет успешного текста.
        text_unsuccessful_color (tuple): RGB цвет неуспешного текста.
        button_enabled_color (tuple): RGB цвет активной кнопки.
        button_disabled_color (tuple): RGB цвет неактивной кнопки.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """
        Создает единственный экземпляр класса (Singleton).

        Returns:
            WindowPattern: Единственный экземпляр класса.
        """
        if cls._instance is None:
            cls._instance = super(WindowPattern, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Инициализирует настройки UI приложения.

        Загружает конфигурацию из JSON-файлов и инициализирует
        цвета, шрифты и другие параметры интерфейса.
        """
        if WindowPattern._initialized:
            return

        self.load_resources()
        self.screen_caption = "Драг Рейсинг"

        self.button_enabled_color = self.text_simple_color
        self.button_disabled_color = (240, 230, 210)

        self.text_small_size = pygame.font.Font(None, 30)
        self.text_middle_size = pygame.font.Font(None, 40)
        self.text_large_size = pygame.font.Font(None, 50)

        WindowPattern._initialized = True

    def load_resources(self):
        """
        Загружает ресурсы UI из конфигурационных JSON-файлов.

        Загружает параметры окна (размер, цвет) и настройки текста
        (цвета для различных состояний) из файлов конфигурации.

        Raises:
            FileNotFoundError: Если конфигурационные файлы не найдены.
            json.JSONDecodeError: Если JSON имеет неверный формат.
            KeyError: Если в JSON отсутствуют необходимые ключи.
        """
        try:
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

        except FileNotFoundError as e:
            print(f"Ошибка: конфигурационный файл не найден: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Ошибка: неверный формат JSON в конфигурационном файле: {e}")
            raise
        except KeyError as e:
            print(f"Ошибка: отсутствует ключ {e} в конфигурационном файле")
            raise

    def get_screen_size(self):
        """
        Возвращает размер окна приложения.

        Returns:
            tuple: Кортеж (ширина, высота) окна в пикселях.
        """
        return self.screen_width, self.screen_height

    def get_screen_color(self):
        """
        Возвращает цвет фона окна.

        Returns:
            tuple: RGB кортеж цвета фона.
        """
        return self.screen_color

    def get_screen_caption(self):
        """
        Возвращает заголовок окна приложения.

        Returns:
            str: Заголовок окна.
        """
        return self.screen_caption

    def get_button_colors(self):
        """
        Возвращает цвета кнопок для активного и неактивного состояний.

        Returns:
            tuple: Кортеж (цвет_активной_кнопки, цвет_неактивной_кнопки).
        """
        return self.button_enabled_color, self.button_disabled_color

    def get_text_colors(self, color='simple'):
        """
        Возвращает цвет текста в зависимости от типа.

        Args:
            color (str): Тип цвета ('simple', 'success', 'unsuccess').
                        По умолчанию 'simple'.

        Returns:
            tuple: RGB кортеж цвета текста.
        """
        colors = {
            'simple': self.text_simple_color,
            'success': self.text_successful_color,
            'unsuccess': self.text_unsuccessful_color
        }
        return colors.get(color, self.text_simple_color)

    def get_font(self, size='medium'):
        """
        Возвращает объект шрифта указанного размера.

        Args:
            size (str): Размер шрифта ('small', 'medium', 'large').
                       По умолчанию 'medium'.

        Returns:
            pygame.font.Font: Объект шрифта Pygame.
        """
        fonts = {
            'small': self.text_small_size,
            'medium': self.text_middle_size,
            'large': self.text_large_size
        }
        return fonts.get(size, self.text_middle_size)


class WindowObject:
    """
    Класс для создания UI-объектов (кнопки, изображения).

    Создает интерактивные элементы интерфейса с поддержкой текста,
    изображений и действий по клику.

    Attributes:
        screen (pygame.Surface): Поверхность экрана для отрисовки.
        coordinate_x (int): X-координата объекта.
        coordinate_y (int): Y-координата объекта.
        surface_width (int): Ширина объекта.
        surface_height (int): Высота объекта.
        radius (int): Радиус скругления углов.
        text (str): Текст на кнопке (если есть).
        image (pygame.Surface): Изображение объекта (если есть).
        action (callable): Функция, вызываемая при клике.
        clicked (bool): Флаг состояния клика.
    """

    _window_pattern = None

    def __init__(self, screen, coordinate_x, coordinate_y, surface_width, surface_height,
                 radius, text=None, image=None, action=None):
        """
        Инициализирует UI-объект.

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
            coordinate_x (int): X-координата объекта.
            coordinate_y (int): Y-координата объекта.
            surface_width (int): Ширина объекта в пикселях.
            surface_height (int): Высота объекта в пикселях.
            radius (int): Радиус скругления углов в пикселях.
            text (str, optional): Текст на объекте. По умолчанию None.
            image (pygame.Surface, optional): Изображение объекта. По умолчанию None.
            action (callable, optional): Функция-обработчик клика. По умолчанию None.
        """
        self.screen = screen
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.surface_width = surface_width
        self.surface_height = surface_height
        self.surface_width_stroke = 2
        self.radius = radius

        if WindowObject._window_pattern is None:
            WindowObject._window_pattern = WindowPattern()

        self.button_on_color = WindowObject._window_pattern.button_enabled_color
        self.button_off_color = WindowObject._window_pattern.button_disabled_color
        self.text = text
        self.font = WindowObject._window_pattern.get_font("small")
        self.image = image
        self.clicked = False
        self.action = action

    def set_image(self, new_image):
        """
        Устанавливает новое изображение для объекта.

        Args:
            new_image (pygame.Surface): Новое изображение.
        """
        self.image = new_image

    def obj_image(self):
        """
        Отрисовывает объект с изображением на экране.

        Создает прямоугольную область со скругленными углами,
        масштабирует изображение под размер области и отрисовывает
        с рамкой на экране.
        """
        surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, self.surface_width, self.surface_height)
        pygame.draw.rect(surface, self.button_on_color, rect, border_radius=self.radius)

        mask = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), rect, border_radius=self.radius)

        scaled_image = pygame.transform.scale(self.image, (self.surface_width, self.surface_height))
        rounded_image = scaled_image.copy()
        rounded_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        surface.blit(rounded_image, (0, 0))

        pygame.draw.rect(surface, (0, 0, 0), rect, self.surface_width_stroke, border_radius=self.radius)
        self.screen.blit(surface, (self.coordinate_x, self.coordinate_y))

    def obj_button_with_text(self):
        """
        Отрисовывает интерактивную кнопку с текстом.

        Создает кнопку, которая меняет цвет при наведении мыши
        и выполняет действие при клике. Обрабатывает состояния
        наведения и клика для предотвращения множественных срабатываний.
        """
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

        if click[0] == 0:
            self.clicked = False

        button_surface.blit(text_surface, text_rect)
        pygame.draw.rect(button_surface, (0, 0, 0), rect, self.surface_width_stroke, border_radius=self.radius)
        self.screen.blit(button_surface, (self.coordinate_x, self.coordinate_y))


class InputBox:
    """
    Класс для создания текстового поля ввода.

    Поддерживает ввод текста и чисел с валидацией,
    визуальную индикацию активного состояния и ошибок ввода.

    Attributes:
        rect (pygame.Rect): Прямоугольная область поля ввода.
        text (str): Текущий текст в поле.
        active (bool): Флаг активности поля (выбрано/не выбрано).
        numbers_only (bool): Флаг режима ввода только чисел.
        is_rgb (bool): Флаг режима ввода RGB значений (0-255).
        is_valid (bool): Флаг валидности введенных данных.
    """

    _window_pattern = None

    def __init__(self, x, y, w, h, text='', numbers_only=False, is_rgb=False):
        """
        Инициализирует поле ввода.

        Args:
            x (int): X-координата поля.
            y (int): Y-координата поля.
            w (int): Ширина поля в пикселях.
            h (int): Высота поля в пикселях.
            text (str, optional): Начальный текст. По умолчанию пустая строка.
            numbers_only (bool, optional): Если True, разрешен ввод только цифр.
                                          По умолчанию False.
            is_rgb (bool, optional): Если True, ограничивает ввод до 3 цифр (0-255).
                                    По умолчанию False.
        """
        if InputBox._window_pattern is None:
            InputBox._window_pattern = WindowPattern()

        self.rect = pygame.Rect(x, y, w, h)
        self.color = InputBox._window_pattern.get_text_colors("simple")
        self.text = text
        self.txt_surface = InputBox._window_pattern.get_font("small").render(text, True, self.color)
        self.active = False
        self.numbers_only = numbers_only
        self.is_rgb = is_rgb
        self.is_valid = True

    def handle_event(self, event):
        """
        Обрабатывает события клавиатуры и мыши для поля ввода.

        Обрабатывает клики мыши для активации/деактивации поля,
        ввод символов с клавиатуры с валидацией и удаление символов.

        Args:
            event (pygame.event.Event): Событие Pygame для обработки.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (InputBox._window_pattern.get_text_colors("success") if self.active
                          else InputBox._window_pattern.get_text_colors("simple"))

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.is_valid = True
                else:
                    if self.numbers_only:
                        if event.unicode.isdigit():
                            if self.is_rgb:
                                if len(self.text) < 3:
                                    self.text += event.unicode
                                    self.is_valid = True
                                else:
                                    self.is_valid = False
                            else:
                                if len(self.text) < 4:
                                    self.text += event.unicode
                                    self.is_valid = True
                                else:
                                    self.is_valid = False
                        else:
                            self.is_valid = False
                    else:
                        self.text += event.unicode
                        self.is_valid = True

                color = (InputBox._window_pattern.get_text_colors("unsuccess") if not self.is_valid
                         else self.color)
                self.txt_surface = InputBox._window_pattern.get_font("small").render(self.text, True, color)

    def update(self):
        """
        Обновляет ширину поля ввода в зависимости от длины текста.

        Расширяет поле автоматически, если текст не помещается,
        с минимальной шириной 200 пикселей.
        """
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        """
        Отрисовывает поле ввода на экране.

        Рисует текст и рамку поля. Цвет рамки меняется на красный
        при невалидном вводе.

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
        """
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        border_color = (InputBox._window_pattern.get_text_colors("unsuccess") if not self.is_valid
                        else self.color)
        pygame.draw.rect(screen, border_color, self.rect, 2)

    def get_value(self):
        """
        Возвращает значение поля ввода.

        Для полей с numbers_only=True пытается преобразовать текст
        в число (int или float). Для текстовых полей возвращает строку.

        Returns:
            int, float, str, or None: Числовое значение для числовых полей,
                                      строка для текстовых полей,
                                      None если преобразование невозможно.
        """
        if self.numbers_only and self.text:
            try:
                return int(self.text)
            except ValueError:
                return None
        return self.text

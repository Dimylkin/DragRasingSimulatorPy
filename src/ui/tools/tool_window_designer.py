import pygame


class ScreenManager:
    """Менеджер экранов для управления переключением между разными состояниями игры"""

    def __init__(self):
        self.screens = {}
        self.current_screen = None
        self.screen_size = (800, 600)

    def add_screen(self, name, screen):
        """Добавляет экран в менеджер"""
        self.screens[name] = screen
        if self.current_screen is None:
            self.current_screen = name

    def switch_screen(self, name):
        """Переключает на указанный экран"""
        if name in self.screens:
            self.current_screen = name
            return True
        return False

    def get_current_screen(self):
        """Возвращает текущий активный экран"""
        return self.screens.get(self.current_screen)

    def update(self):
        """Обновляет текущий экран"""
        current = self.get_current_screen()
        if current:
            current.update()

    def draw(self, surface):
        """Отрисовывает текущий экран"""
        current = self.get_current_screen()
        if current:
            current.draw(surface)


class Button:
    def __init__(self, screen, coordinate_x, coordinate_y, surface_width, surface_height, surface_width_stroke
                 , button_radius, button_on_color, button_off_color, button_text = None, button_image = None, action = None):
        self.screen = screen
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.surface_width = surface_width
        self.surface_height = surface_height
        self.surface_width_stroke = surface_width_stroke
        self.button_radius = button_radius
        self.button_on_color = button_on_color
        self.button_off_color = button_off_color
        self.button_text = button_text
        self.font = pygame.font.Font(None, 30)
        self.button_image = button_image
        self.clicked = False
        self.action = action

    def button_with_image(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, self.surface_width, self.surface_height)
        screen_rect = pygame.Rect(self.coordinate_x, self.coordinate_y, self.surface_width, self.surface_height)
        on_button = screen_rect.collidepoint(mouse)

        if on_button:
            pygame.draw.rect(button_surface, self.button_on_color, rect, border_radius = self.button_radius)

            if click[0] == 1 and not self.clicked:
                self.clicked = True
                if self.action:
                    print(f"Выполняется действие: {self.action}")
                    self.action()

        else:
            pygame.draw.rect(button_surface, self.button_off_color, rect, border_radius = self.button_radius)
            self.clicked = False

        mask = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), rect, border_radius = self.button_radius)

        scaled_img = pygame.transform.scale(self.button_image, (self.surface_width, self.surface_height))
        rounded_img = scaled_img.copy()
        rounded_img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        button_surface.blit(rounded_img, (0, 0))

        pygame.draw.rect(button_surface, (0, 0, 0), rect, self.surface_width_stroke, border_radius = self.button_radius)

        self.screen.blit(button_surface, (self.coordinate_x, self.coordinate_y))


    def button_with_text(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, self.surface_width, self.surface_height)
        screen_rect = pygame.Rect(self.coordinate_x, self.coordinate_y, self.surface_width, self.surface_height)
        on_button = screen_rect.collidepoint(mouse)

        text_surface = self.font.render(self.button_text, True, (0, 0, 0))

        text_rect = text_surface.get_rect(center=(self.surface_width // 2, self.surface_height // 2))

        if on_button:
            pygame.draw.rect(button_surface, self.button_on_color, rect, border_radius=self.button_radius)

            if click[0] == 1 and not self.clicked:
                self.clicked = True
                if self.action:
                    print(f"Выполняется действие: {self.action}")
                    self.action()

        else:
            pygame.draw.rect(button_surface, self.button_off_color, rect, border_radius=self.button_radius)
            self.clicked = False

        button_surface.blit(text_surface, text_rect)

        pygame.draw.rect(button_surface, (0, 0, 0), rect, self.surface_width_stroke, border_radius=self.button_radius)

        self.screen.blit(button_surface, (self.coordinate_x, self.coordinate_y))
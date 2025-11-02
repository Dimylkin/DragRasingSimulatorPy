import pygame
import sys

from src.ui.tools.tool_window_designer import WindowObject, WindowPattern
from src.utils.utils_paths import Utils

class WindowStatistic:
    def __init__(self, user):
        pygame.init()

        window = WindowPattern()
        
        self.screen = pygame.display.set_mode(window.get_screen_size())
        pygame.display.set_caption(window.get_screen_caption())
        self.screen_fill = window.get_screen_color()
        self.screen.fill(self.screen_fill)
        
        self.font_large = window.get_font("large")
        self.text_simple_color = window.get_text_colors("simple")

        self.user = user
        self._load_resource()

        self.is_running = True
        self.clock = pygame.time.Clock()

    def _load_resource(self):
        self.user_image = pygame.image.load(Utils().get_resource_path('images', 'users', self.user.image))

        self.user_avatar = WindowObject(self.screen, 300, 80, 200, 200,
                                        100, None, self.user_image)

        self.text_user_name = self.font_large.render(f"Имя: {self.user.nickname}", True, self.text_simple_color)

        self.text_user_score = self.font_large.render(f"Текущее количество очков: {self.user.score}", True,
                                                      self.text_simple_color)
        self.button_back = WindowObject(self.screen, 30, 20, 75, 30,
                                        5, "Назад", None, self.window_back)

    def window_back(self):
        from src.ui.windows.window_start import WindowStart
        start = WindowStart(self.user)
        self.is_running = False
        start.run()

    def draw(self):
        self.screen.fill(self.screen_fill)

        self.button_back.obj_button_with_text()
        self.user_avatar.obj_image()

        rect_name = self.text_user_name.get_rect(center=(400, 320))
        self.screen.blit(self.text_user_name, rect_name)

        rect_score = self.text_user_score.get_rect(center=(400, 370))
        self.screen.blit(self.text_user_score, rect_score)

        title = self.font_large.render("Статистика игрока", True, self.text_simple_color)
        rect_title = title.get_rect(center=(400, 40))
        self.screen.blit(title, rect_title)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

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



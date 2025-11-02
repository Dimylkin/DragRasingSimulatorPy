import sys
import pygame

from src.ui.tools.tool_window_designer import WindowObject, WindowPattern
from src.ui.windows.window_race_manager import RaceManager
from src.utils.utils_paths import Utils
from src.game.game_car import Car
from src.ui.windows.window_track_manager import WindowBackgroundSegments


class RaceSettings:
    def __init__(self, user):
        pygame.init()
        window = WindowPattern()

        self.screen = pygame.display.set_mode(window.get_screen_size())
        pygame.display.set_caption(window.get_screen_caption())
        self.screen_fill = window.get_screen_color()
        self.screen.fill(self.screen_fill)

        self.font_large = window.get_font("large")
        self.font_middle = window.get_font("middle")
        self.font_small = window.get_font("small")

        self.text_color_simple = window.get_text_colors("simple")
        self.text_color_success = window.get_text_colors("success")
        self.text_color_unsuccess = window.get_text_colors("unsuccess")

        self.user = user

        self.list_tracks = []
        for track in Utils().get_list_tracks():
            self.list_tracks.append(WindowBackgroundSegments(self.screen, track, self.user))

        self.list_cars = []
        for car in Utils().get_list_cars():
            self.list_cars.append(Car(car))

        self.track_current_index = 0
        self.car_current_index = 0
        self.user_score = 0


        self._load_resources()

        self.is_not_locked_car = False
        self.is_not_locked_track = False
        self.is_running = True

        self.clock = pygame.time.Clock()

    def _load_resources(self):
        self.track_current = self.list_tracks[self.track_current_index]
        self.car_current = self.list_cars[self.car_current_index]

        self.is_not_locked_car = self.get_status_access_to_car()
        self.is_not_locked_track = self.get_status_access_to_track()

        self.image_track = pygame.image.load(
            Utils().get_resource_path('images', 'tracks', self.track_current.image)).convert_alpha()

        self.image_car = pygame.image.load(
            Utils().get_resource_path('images', 'cars', self.car_current.first_image)).convert_alpha()

        self.button_back = WindowObject(self.screen, 30, 20, 75, 30,
                                        5, "Назад", None, self.back)

        self.button_track_left_choice = WindowObject(self.screen, 100, 115, 30, 30,
                                                     10, "<", None, self.previous_track)

        self.button_track = WindowObject(self.screen, 140, 80, 200, 100,
                                         15, None, self.image_track)

        self.button_track_right_choice = WindowObject(self.screen, 350, 115, 30, 30,
                                                      10, ">", None, self.next_track)

        self.button_car_left_choice = WindowObject(self.screen, 100, 320, 30, 30,
                                                   10, "<", None, self.previous_car)

        self.button_car = WindowObject(self.screen, 140, 280, 200, 100,
                                       15, None, self.image_car)

        self.button_car_right_choice = WindowObject(self.screen, 350, 320, 30, 30,
                                                    10, ">", None, self.next_car)

        self.button_mode_bot = WindowObject(self.screen, 200, 480, 200, 100,
                                            15, "Игра с ботом", None)

        self.button_mode_alone = WindowObject(self.screen, 450, 480, 200, 100,
                                              15, "Одиночная игра", None, self.switch_to_race)

        self.text_choice_track = self.font_middle.render("Выберите карту", True, self.text_color_simple)
        self.text_choice_car = self.font_middle.render("Выберите машину", True, self.text_color_simple)
        self.text_choice_mode = self.font_middle.render("Выберите режим игры", True, self.text_color_simple)

        self._update_current_texts()

    def get_status_access_to_car(self):
        return self.user.score >= self.car_current.score_to_unlocking

    def get_status_access_to_track(self):
        return self.user.score >= self.track_current.score_to_unlocking

    def back(self):
        from src.ui.windows.window_start import WindowStart
        start = WindowStart(self.user)
        self.is_running = False
        start.run()

    def previous_track(self):
        self.track_current_index = (self.track_current_index - 1) % len(self.list_tracks)
        self._update_track()

    def next_track(self):
        self.track_current_index = (self.track_current_index + 1) % len(self.list_tracks)
        self._update_track()

    def previous_car(self):
        self.car_current_index = (self.car_current_index - 1) % len(self.list_cars)
        self._update_car()

    def next_car(self):
        self.car_current_index = (self.car_current_index + 1) % len(self.list_cars)
        self._update_car()

    def _update_track(self):
        self.track_current = self.list_tracks[self.track_current_index]

        try:
            new_image = pygame.image.load(
                Utils().get_resource_path('images', 'tracks', self.track_current.image)).convert_alpha()
            self.button_track.set_image(new_image)
        except Exception as e:
            print(f"Ошибка загрузки карты {self.track_current}: {e}")

        self.is_not_locked_track = self.get_status_access_to_track()
        self._update_current_texts()

    def _update_car(self):
        self.car_current = self.list_cars[self.car_current_index]

        try:
            new_image = pygame.image.load(
                Utils().get_resource_path('images', 'cars', self.car_current.first_image)).convert_alpha()
            self.button_car.set_image(new_image)
        except Exception as e:
            print(f"Ошибка загрузки машины {self.car_current}: {e}")

        self.is_not_locked_car = self.get_status_access_to_car()
        self._update_current_texts()

    def _update_current_texts(self):

        self.text_track_current = self.font_small.render(f"Карта: {self.track_current.name}", True, self.text_color_simple)
        self.text_car_current = self.font_small.render(f"Машина: {self.car_current.name}", True, self.text_color_simple)
        self.text_car_current_hp = self.font_small.render(f"• Лошадиных сил: {self.car_current.horse_power}", True, self.text_color_simple)
        self.text_car_current_min_rev = self.font_small.render(f"• Минимальные обороты: {self.car_current.min_revolutions}", True,
                                                           self.text_color_simple)
        self.text_car_current_max_rev = self.font_small.render(f"• Максимальные обороты: {self.car_current.max_revolutions}", True,
                                                           self.text_color_simple)
        self.text_car_current_max_speed = self.font_small.render(f"• Максимальная скорость: {self.car_current.max_speed}", True,
                                                             self.text_color_simple)

        if self.is_not_locked_car:
            self.text_access_to_car = self.font_small.render("Машина: Доступна!", True, self.text_color_success)
        else:
            self.text_access_to_car_line1 = self.font_small.render("Машина: Не доступна!", True, self.text_color_unsuccess)
            self.text_access_to_car_line2 = self.font_small.render(f"Ваши очки: {self.user_score}", True, self.text_color_unsuccess)
            self.text_access_to_car_line3 = self.font_small.render(f"Нужно очков: {self.car_current.score_to_unlocking}", True,
                                                               self.text_color_unsuccess)

        if self.is_not_locked_track:
            self.text_access_to_track = self.font_small.render("Карта: Доступна!", True, self.text_color_success)
        else:
            self.text_access_to_track_line1 = self.font_small.render("Карта: Не доступна!", True, self.text_color_unsuccess)
            self.text_access_to_track_line2 = self.font_small.render(f"Ваши очки: {self.user_score}", True, self.text_color_unsuccess)
            self.text_access_to_track_line3 = self.font_small.render(f"Нужно очков: {self.track_current.score_to_unlocking}", True,
                                                                 self.text_color_unsuccess)

    def switch_to_race(self):
        if self.is_not_locked_car and self.is_not_locked_track:
            race_manager = RaceManager(self.car_current, self.track_current, self.user)
            self.is_running = False
            race_manager.run()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _draw(self):
        self.screen.fill(self.screen_fill)

        self.button_back.obj_button_with_text()

        self.screen.blit(self.text_choice_track, (130, 20))
        self.button_track_left_choice.obj_button_with_text()
        self.button_track.obj_image()
        self.button_track_right_choice.obj_button_with_text()

        self.screen.blit(self.text_choice_car, (130, 220))
        self.button_car_left_choice.obj_button_with_text()
        self.button_car.obj_image()
        self.button_car_right_choice.obj_button_with_text()

        self.screen.blit(self.text_choice_mode, (280, 420))
        self.button_mode_bot.obj_button_with_text()
        self.button_mode_alone.obj_button_with_text()

        self.separator = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(420, 10, 2, 380))

        self.screen.blit(self.text_track_current, (450, 20))
        self.screen.blit(self.text_car_current, (450, 50))
        self.screen.blit(self.text_car_current_hp, (450, 80))
        self.screen.blit(self.text_car_current_min_rev, (450, 110))
        self.screen.blit(self.text_car_current_max_rev, (450, 140))
        self.screen.blit(self.text_car_current_max_speed, (450, 170))

        y_offset_car = 200
        if self.is_not_locked_car:
            self.screen.blit(self.text_access_to_car, (450, y_offset_car))
        else:
            self.screen.blit(self.text_access_to_car_line1, (450, y_offset_car))
            self.screen.blit(self.text_access_to_car_line2, (450, y_offset_car + 30))
            self.screen.blit(self.text_access_to_car_line3, (450, y_offset_car + 60))

        y_offset_track = 290
        if self.is_not_locked_track:
            self.screen.blit(self.text_access_to_track, (450, y_offset_track))
        else:
            self.screen.blit(self.text_access_to_track_line1, (450, y_offset_track))
            self.screen.blit(self.text_access_to_track_line2, (450, y_offset_track + 30))
            self.screen.blit(self.text_access_to_track_line3, (450, y_offset_track + 60))

    def run(self):
        while self.is_running:
            self.is_not_locked_car = self.get_status_access_to_car()
            self.is_not_locked_track = self.get_status_access_to_track()
            self._handle_events()
            self._draw()

            pygame.display.flip()
            self.clock.tick(60)
        self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
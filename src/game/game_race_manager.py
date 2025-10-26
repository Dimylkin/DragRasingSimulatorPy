import datetime
import pygame
import sys

from src.utils.utils_paths import get_asset_path, get_resource_path
from src.game.game_car import Car
from src.ui.windows.window_track_manager import Background, LongRoad


class RaceManager:
    def __init__(self):
        pygame.init()

        self._screen_width, self._screen_height = 800, 600
        self._FONT = pygame.font.Font(None, 36)

        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        pygame.display.set_caption("Драг рейсинг")
        self._load_resources()
        self._create_instances()

        self.speeds = [0]
        self.warning_frames = 0
        self.after_shift_frames = 0
        self._is_running = True
        self._is_good_shift = True
        self._is_finished = False

        self._clock = pygame.time.Clock()
        self.time_start_race = None

    def _load_resources(self):
        self._image_track = get_resource_path('images', 'tracks', 'track_rainy_swedish_road.jpg')
        # Для машины загружаем JSON файл с характеристиками
        self._car_data_path = get_asset_path('cars', 'car_audi_rs6.json')

    def _create_instances(self):
        self._road = LongRoad(self._screen, self._image_track)
        self._car = Car("audi_rs6")  # Передаем имя машины для загрузки
        self._cars = pygame.sprite.Group()
        self._cars.add(self._car)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        if event.key == pygame.K_UP and self.after_shift_frames <= 0 and not self._is_finished:
            current_gear = self._car.current_gear
            if current_gear < self._car.engine.count_gear:
                new_gear = current_gear + 1
                self._is_good_shift = self._car.shift_gear(new_gear)
                self.after_shift_frames = 60

                if not self._is_good_shift:
                    self.warning_frames = 60
                    self.after_shift_frames = 120

    def _update_game_state(self):
        if self._is_finished:
            return

        self._car.update(self._is_good_shift)
        self.speeds.append(self._car.engine.get_current_speed())

        if self.warning_frames > 0:
            self.warning_frames -= 1

        if self.after_shift_frames > 0:
            self.after_shift_frames -= 1

        self._is_finished = self._road.update(self._car.speed)

    def _draw(self):
        self._road.draw(self._screen)
        self._cars.draw(self._screen)

        # Используем статические методы Background
        Background.draw_hud(self._screen, self._car, 10, 30, 200, 20)

        if self.warning_frames > 0:
            Background.draw_not_good_shift(self._screen, self._screen_width, self._screen_height)  # ← Исправлены параметры

        if self._is_finished:
            Background.draw_finish(self._screen, self._screen_width, self._screen_height,
                                   self.time_start_race, self.speeds)
            self._is_running = False  # ← Исправлено: было self.is_running

    def start_race(self):
        self._car.start_engine()
        self.time_start_race = datetime.datetime.now()

    def run(self):
        self.start_race()

        while self._is_running:
            self._handle_events()
            self._update_game_state()
            self._draw()

            pygame.display.flip()
            self._clock.tick(60)

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()
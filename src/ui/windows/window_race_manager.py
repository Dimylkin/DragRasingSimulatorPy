import datetime
import pygame
import sys

from src.ui.windows.window_track_manager import Background, WindowBackgroundSegments
from src.ui.tools.tool_window_designer import WindowPattern


class RaceManager:
    def __init__(self, car, track, user):
        pygame.init()
        window = WindowPattern()
        self.user = user
        self._screen_width, self._screen_height = window.get_screen_size()

        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        pygame.display.set_caption(window.get_screen_caption())
        self.car = car
        self.track = track
        self.track.screen = self._screen
        self._create_instances()

        self.speeds = [0]
        self.count_lose_shift = 0

        self.frames_warning = 0
        self.frames_after_shift = 0

        
        self._is_running = True
        self._is_good_shift = True
        self._is_boost = False
        self._is_finished = False
        self.is_time_start_race = None

        self._clock = pygame.time.Clock()

    def _create_instances(self):
        self._road = self.track
        self._car = self.car
        self._cars = pygame.sprite.Group()
        self._cars.add(self._car)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        if event.key == pygame.K_UP and self.frames_after_shift <= 0 and not self._is_finished:
            current_gear = self._car.current_gear
            if current_gear < self._car.engine.count_gear:
                new_gear = current_gear + 1
                self._is_good_shift = self._car.shift_gear(new_gear)
                self._is_boost = self._car.engine.is_boost()
                self.frames_after_shift = self._car.frames_after_shift

                if not self._is_good_shift:
                    self.count_lose_shift += 1
                    self.frames_warning = 60
                    self.frames_after_shift = self._car.frames_after_shift

    def _update_game_state(self):
        if self._is_finished:
            return

        self._car.update(self._is_good_shift)
        self.frames_boost = self._car.boost_frames_remaining
        self.speeds.append(self._car.engine.get_current_speed())

        if self.frames_warning > 0:
            self.frames_warning -= 1

        if self.frames_after_shift > 0:
            self.frames_after_shift -= 1

        self._is_finished = self._road.update(self._car.speed)

    def _draw(self):
        self._road.draw(self._screen)
        self._cars.draw(self._screen)

        Background.draw_hud(self._screen, self._car, 10, 30, 200, 20)

        if self.frames_warning > 0:
            Background.draw_not_good_shift(self._screen, self._screen_width, self._screen_height)

        if self.frames_boost > 0:
            Background.draw_boost(self._screen, self._screen_width, self._screen_height)

        if self._is_finished:
            Background.draw_finish(self._screen, self._screen_width, self._screen_height,
                                   self.is_time_start_race, self.speeds, self.count_lose_shift, self.user)
            from src.ui.windows.window_start import WindowStart
            start = WindowStart(self.user)
            self._is_running = False
            start.run()

    def start_race(self):
        self._car.start_engine()
        self.is_time_start_race = datetime.datetime.now()

    def run(self):
        self.start_race()

        while self._is_running:
            self._handle_events()
            self._update_game_state()
            self._draw()

            pygame.display.flip()
            self._clock.tick(60)

        self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
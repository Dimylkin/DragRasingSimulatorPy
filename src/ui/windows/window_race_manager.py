"""
Модуль управления гонкой.

Содержит класс RaceManager для управления игровым процессом гонки,
включая обработку событий, обновление состояния игры и отрисовку.
"""

import datetime
import sys

import pygame

from src.ui.tools.tool_window_designer import WindowPattern
from src.ui.windows.window_track_manager import Background


class RaceManager:
    """
    Класс менеджера гонки.

    Управляет игровым процессом гонки: обрабатывает ввод пользователя,
    обновляет состояние автомобиля и трека, отрисовывает игровые элементы
    и подсчитывает результаты гонки.

    Attributes:
        user: Объект пользователя.
        car (Car): Объект автомобиля игрока.
        track: Объект трека гонки.
        speeds (list): Список скоростей для расчета средней скорости.
        count_lose_shift (int): Количество неудачных переключений передач.
        frames_warning (int): Таймер отображения предупреждения о плохом переключении.
        frames_after_shift (int): Таймер блокировки переключения после переключения передачи.
        is_time_start_race (datetime.datetime): Время начала гонки.
    """

    def __init__(self, car, track, user, stock_car_for_mode=None):
        """
        Инициализирует менеджер гонки.

        Args:
            car (Car): Объект автомобиля игрока.
            track: Объект трека гонки.
            user: Объект пользователя.
            stock_car_for_mode: Дополнительный автомобиль для определенных режимов (не используется).
        """
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
        self.frames_boost = 0

        self._is_running = True
        self._is_good_shift = True
        self._is_boost = False
        self._is_finished = False
        self.is_time_start_race = None

        self._clock = pygame.time.Clock()

    def _create_instances(self):
        """
        Создает игровые объекты и группы спрайтов.

        Инициализирует дорогу, автомобиль и группу спрайтов для отрисовки.
        """
        self._road = self.track
        self._car = self.car
        self._cars = pygame.sprite.Group()
        self._cars.add(self._car)

    def _handle_events(self):
        """
        Обрабатывает события Pygame.

        Обрабатывает события закрытия окна и нажатия клавиш.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        """
        Обрабатывает события нажатия клавиш.

        Обрабатывает переключение передач по нажатию стрелки вверх,
        проверяет корректность переключения и устанавливает флаги буста.

        Args:
            event (pygame.event.Event): Событие нажатия клавиши.
        """
        if event.key == pygame.K_UP and self.frames_after_shift <= 0 and not self._is_finished:
            current_gear = self._car.current_gear
            if current_gear < self._car.engine.count_gear:
                new_gear = current_gear + 1

                self._is_boost = self._car.engine.is_boost()
                self._is_good_shift = self._car.shift_gear(new_gear)
                self.frames_after_shift = self._car.frames_after_shift

                if not self._is_good_shift:
                    self.count_lose_shift += 1
                    self.frames_warning = 60

    def _update_game_state(self):
        """
        Обновляет состояние игры на каждом кадре.

        Обновляет состояние автомобиля, записывает текущую скорость,
        обновляет таймеры и проверяет завершение гонки.
        """
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
        """
        Отрисовывает все элементы игры.

        Рисует дорогу, автомобиль, HUD, предупреждения, индикатор буста
        и экран финиша при завершении гонки.
        """
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
            pygame.display.flip()
            pygame.time.wait(3000)

            from src.ui.windows.window_start import WindowStart
            start = WindowStart(self.user)
            self._is_running = False
            start.run()

    def start_race(self):
        """
        Запускает гонку.

        Инициирует ускорение двигателя автомобиля и фиксирует время старта.
        """
        self._car.start_engine()
        self.is_time_start_race = datetime.datetime.now()

    def run(self):
        """
        Запускает главный игровой цикл.

        Обрабатывает события, обновляет состояние игры и отрисовывает кадры
        с частотой 60 FPS до завершения гонки или закрытия окна.
        """
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
        """
        Завершает работу Pygame и выходит из программы.
        """
        pygame.quit()
        sys.exit()
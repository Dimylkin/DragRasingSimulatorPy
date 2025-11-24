"""
Модуль управления фоном и треком гонки.

Содержит классы WindowBackgroundSegments и Background для управления
отрисовкой трека, расчета пройденного расстояния и отображения HUD.
"""

import pygame
import datetime
import json

from src.ui.tools.tool_window_designer import WindowPattern
from src.utils.utils_paths import Utils


class WindowBackgroundSegments:
    """
    Класс управления сегментами фона трека.

    Управляет прокруткой фона, состоящего из повторяющихся сегментов,
    отслеживает пройденное расстояние и определяет завершение гонки.

    Attributes:
        screen (pygame.Surface): Поверхность экрана для отрисовки.
        segments (pygame.sprite.Group): Группа спрайтов сегментов фона.
        distance_traveled (float): Пройденное расстояние в метрах.
        distance_total (float): Общая длина трека в метрах.
        is_finished (bool): Флаг завершения гонки.
        name (str): Название трека.
        score_to_unlocking (int): Количество очков для разблокировки трека.
    """

    def __init__(self, screen, name, user):
        """
        Инициализирует систему фоновых сегментов трека.

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
            name (str): Идентификатор трека для загрузки конфигурации.
            user: Объект пользователя.
        """
        self.screen = screen

        self.segments = pygame.sprite.Group()
        self.segment_width = self.screen.get_width()
        self.segments_total = 5

        self.user = user
        self._load_data_track(name)

        for i in range(self.segments_total):
            segment = Background(self.screen, self.image, self.user)
            segment.rect.x = i * self.screen.get_width()
            self.segments.add(segment)

        self.distance_traveled = 0
        self.distance_total = 4020

        self._is_finished = False

    def _load_data_track(self, name):
        """
        Загружает данные трека из JSON-файла.

        Args:
            name (str): Идентификатор трека.

        Raises:
            FileNotFoundError: Если файл трека не найден.
            json.JSONDecodeError: Если JSON имеет неверный формат.
            KeyError: Если в JSON отсутствуют необходимые ключи.
        """
        try:
            with open(Utils().get_asset_path('tracks', f'track_{name}.json'), 'r',
                      encoding='utf-8') as asset_track:
                data = json.load(asset_track)
                self.image = data['image']
                self.name = data['name']
                self.score_to_unlocking = data['score_to_unlocking']
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Ошибка загрузки данных трека '{name}': {e}")
            raise

    def update(self, car_speed):
        """
        Обновляет положение сегментов фона на основе скорости автомобиля.

        Перемещает сегменты влево для создания эффекта движения,
        пересоздает сегменты, вышедшие за пределы экрана, справа
        и отслеживает пройденное расстояние.

        Args:
            car_speed (float): Текущая скорость автомобиля.

        Returns:
            bool: True, если гонка завершена; False в противном случае.
        """
        if self._is_finished:
            return True

        self.distance_traveled += car_speed * 0.1

        if self.distance_traveled >= self.distance_total:
            self._is_finished = True
            return True

        for segment in self.segments:
            segment.rect.x -= car_speed

            if segment.rect.x <= -self.segment_width:
                max_x = max(s.rect.x for s in self.segments)
                segment.rect.x = max_x + self.segment_width

        return False

    def draw(self, screen):
        """
        Отрисовывает все сегменты фона на экране.

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
        """
        self.segments.draw(screen)

class Circle(pygame.sprite.Sprite):
    def __init__(self, color, center):
        super().__init__()
        self.color = color
        self.center = center

    def traffic_circle(self, screen, radius=25):
        pygame.draw.circle(screen, self.color, self.center, radius)

    def set_color(self, new_color):
        self.color = new_color

class Background(pygame.sprite.Sprite):
    """
    Класс фонового сегмента трека.

    Представляет один сегмент фона, который повторяется для создания
    эффекта бесконечной дороги. Также содержит статические методы
    для отрисовки HUD, сообщений и финишного экрана.

    Attributes:
        screen (pygame.Surface): Поверхность экрана.
        image (pygame.Surface): Изображение сегмента фона.
        rect (pygame.Rect): Прямоугольная область сегмента.
    """

    def __init__(self, screen, image, user):
        """
        Инициализирует сегмент фона.

        Args:
            screen (pygame.Surface): Поверхность экрана.
            image (str): Имя файла изображения фона.
            user: Объект пользователя.
        """
        super().__init__()
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_width(), self.screen.get_height()

        self.image_path = Utils().get_resource_path('images', 'tracks', image)
        self.load_image()

        self.user = user

    def load_image(self):
        """
        Загружает и масштабирует изображение фона.

        Raises:
            FileNotFoundError: Если файл изображения не найден.
            pygame.error: Если возникла ошибка загрузки изображения.
        """
        try:
            self.image_original = pygame.image.load(self.image_path).convert()
            self.image = pygame.transform.scale(self.image_original,
                                                (self.screen_width, self.screen_height))
            self.rect = self.image.get_rect()
        except (FileNotFoundError, pygame.error) as e:
            print(f"Ошибка загрузки изображения фона: {e}")
            self.image = pygame.Surface((self.screen_width, self.screen_height))
            self.image.fill((50, 50, 50))
            self.rect = self.image.get_rect()

    @staticmethod
    def draw_hud(screen, car, x, y, width, height):
        """
        Отрисовывает HUD с информацией о состоянии автомобиля.

        Рисует шкалу оборотов с цветовой индикацией, маркеры зон
        переключения и буста, а также текстовую информацию о передаче и скорости.

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
            car (Car): Объект автомобиля.
            x (int): X-координата шкалы оборотов.
            y (int): Y-координата шкалы оборотов.
            width (int): Ширина шкалы оборотов.
            height (int): Высота шкалы оборотов.
        """
        info = car.get_engine_info()

        font_small = WindowPattern().get_font("small")
        text_color_simple = WindowPattern().get_text_colors("simple")
        text_color_success = WindowPattern().get_text_colors("success")
        text_color_unsuccess = WindowPattern().get_text_colors("unsuccess")

        text_gear = font_small.render(f"Текущая передача: {info['gear']}", True, text_color_simple)
        text_speed = font_small.render(f"Скорость: {info['speed_kmh']} км/ч", True, text_color_simple)

        rpm = car.engine.revolutions

        rpm_max = car.engine.max_revolutions
        rpm_max_to_good_shift = car.engine.max_revolutions_to_good_shift
        rpm_max_to_boost = car.engine.max_revolutions_to_boost

        rpm_min_to_good_shift = car.engine.min_revolutions_to_good_shift
        rpm_min_to_boost = car.engine.min_revolutions_to_boost

        progress = rpm / rpm_max

        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))

        fill_width = int(width * progress)

        if rpm_min_to_good_shift <= rpm <= rpm_max_to_good_shift:
            color = text_color_success
        else:
            color = text_color_unsuccess

        pygame.draw.rect(screen, color, (x, y, fill_width, height))

        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), 2)

        text_rpm = font_small.render(f"Обороты: {round(rpm)}", True, text_color_simple)

        redline_start_good_shift = x + int(width * rpm_max_to_good_shift / rpm_max)
        redline_end_good_shift = x + int(width * rpm_min_to_good_shift / rpm_max)

        blueline_start_boost = x + int(width * rpm_max_to_boost / rpm_max)
        blueline_end_boost = x + int(width * rpm_min_to_boost / rpm_max)

        pygame.draw.line(screen, (255, 0, 0), (redline_start_good_shift, y), (redline_start_good_shift, y + height), 2)
        pygame.draw.line(screen, (255, 0, 0), (redline_end_good_shift, y), (redline_end_good_shift, y + height), 2)

        pygame.draw.line(screen, (0, 0, 255), (blueline_start_boost, y), (blueline_start_boost, y + height), 2)
        pygame.draw.line(screen, (0, 0, 255), (blueline_end_boost, y), (blueline_end_boost, y + height), 2)

        screen.blit(text_rpm, (x, y - 25))
        screen.blit(text_gear, (10, 60))
        screen.blit(text_speed, (10, 90))

    @staticmethod
    def draw_not_good_shift(screen, width, height):
        """
        Отрисовывает предупреждение о плохом переключении передачи.

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
            width (int): Ширина экрана.
            height (int): Высота экрана.
        """
        font_small = WindowPattern().get_font("small")
        text_color_unsuccess = WindowPattern().get_text_colors("unsuccess")
        text_not_good_shift = font_small.render("!Плохое переключение передачи! Потеря мощности!", True,
                                                text_color_unsuccess)
        screen.blit(text_not_good_shift, ((width / 4) - 20, (height / 4) + 80))

    @staticmethod
    def draw_boost(screen, width, height):
        """
        Отрисовывает сообщение об активации буста.

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
            width (int): Ширина экрана.
            height (int): Высота экрана.
        """
        font_small = WindowPattern().get_font("small")
        text_color_success = WindowPattern().get_text_colors("success")
        text_boost = font_small.render("!Прекрасное переключение! Буст активирован!", True, text_color_success)
        screen.blit(text_boost, ((width / 4) - 20, (height / 4) + 80))

    @staticmethod
    def traffic(screen, state):
        """
        Отрисовывает светофор с состояниями: red, yellow, green.

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
            state (str): Состояние светофора - "red", "yellow_1", "yellow_2", "yellow_3", "green".
        """

        rect_x = screen.get_width() - 175
        rect_y = 100
        rect_width = 150
        rect_height = 320
        pygame.draw.rect(screen, (82,82,82), (rect_x, rect_y, rect_width, rect_height), border_radius=20)

        radius = 15
        offset_x1 = rect_x + 40
        offset_x2 = rect_x + 110
        pos_y = [rect_y + 50, rect_y + 100, rect_y + 150, rect_y + 200, rect_y + 250]

        if state == "red":
            yellow_color_1 = (0, 0, 0)
            yellow_color_2 = (0, 0, 0)
            yellow_color_3 = (0, 0, 0)
            green_color = (0, 0, 0)
            red_color = (255, 0, 0)
        elif state == "yellow_1":
            yellow_color_1 = (255, 255, 0)
            yellow_color_2 = (0, 0, 0)
            yellow_color_3 = (0, 0, 0)
            green_color = (0, 0, 0)
            red_color = (0, 0, 0)
        elif state == "yellow_2":
            yellow_color_1 = (255, 255, 0)
            yellow_color_2 = (255, 255, 0)
            yellow_color_3 = (0, 0, 0)
            green_color = (0, 0, 0)
            red_color = (0, 0, 0)
        elif state == "yellow_3":
            yellow_color_1 = (255, 255, 0)
            yellow_color_2 = (255, 255, 0)
            yellow_color_3 = (255, 255, 0)
            green_color = (0, 0, 0)
            red_color = (0, 0, 0)
        elif state == "green":
            yellow_color_1 = (0, 0, 0)
            yellow_color_2 = (0, 0, 0)
            yellow_color_3 = (0, 0, 0)
            green_color = (0, 255, 0)
            red_color = (0, 0, 0)
        elif state == "red":
            yellow_color_1 = (0, 0, 0)
            yellow_color_2 = (0, 0, 0)
            yellow_color_3 = (0, 0, 0)
            green_color = (0, 0, 0)
            red_color = (255, 0, 0)
        else:
            yellow_color_1 = (0, 0, 0)
            yellow_color_2 = (0, 0, 0)
            yellow_color_3 = (0, 0, 0)
            green_color = (0, 0, 0)
            red_color = (0, 0, 0)


        circle_yellow_1_1 = Circle(yellow_color_1, (offset_x1, pos_y[0]))
        circle_yellow_1_1.traffic_circle(screen, radius)
        circle_yellow_1_2 = Circle(yellow_color_1, (offset_x2, pos_y[0]))
        circle_yellow_1_2.traffic_circle(screen, radius)

        circle_yellow_2_1 = Circle(yellow_color_2, (offset_x1, pos_y[1]))
        circle_yellow_2_1.traffic_circle(screen, radius)
        circle_yellow_2_2 = Circle(yellow_color_2, (offset_x2, pos_y[1]))
        circle_yellow_2_2.traffic_circle(screen, radius)

        circle_yellow_3_1 = Circle(yellow_color_3, (offset_x1, pos_y[2]))
        circle_yellow_3_1.traffic_circle(screen, radius)
        circle_yellow_3_2 = Circle(yellow_color_3, (offset_x2, pos_y[2]))
        circle_yellow_3_2.traffic_circle(screen, radius)

        circle_green_4_1 = Circle(green_color, (offset_x1, pos_y[3]))
        circle_green_4_1.traffic_circle(screen, radius)
        circle_green_4_2 = Circle(green_color, (offset_x2, pos_y[3]))
        circle_green_4_2.traffic_circle(screen, radius)

        circle_red_5_1 = Circle(red_color, (offset_x1, pos_y[4]))
        circle_red_5_1.traffic_circle(screen, radius)
        circle_red_5_2 = Circle(red_color, (offset_x2, pos_y[4]))
        circle_red_5_2.traffic_circle(screen, radius)

    @staticmethod
    def draw_start(screen):
        """
        Отрисовывает на экране надпись "СТАРТ".

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
        """
        font_large = WindowPattern().get_font("large")
        text_color_success = WindowPattern().get_text_colors("success")

        text = font_large.render("СТАРТ", True, text_color_success)
        rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, rect)

    @staticmethod
    def draw_false_start(screen):
        """
        Отрисовывает на экране надпись "ФАЛЬШСТАРТ".

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
        """
        font_large = WindowPattern().get_font("large")
        text_color_error = WindowPattern().get_text_colors("unsuccess")

        text = font_large.render("ФАЛЬШСТАРТ", True, text_color_error)
        rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, rect)

    @staticmethod
    def draw_finish(screen, width, height, time_start_race, is_false_start, speeds, count_lose_shift, car, user):
        """
        Отрисовывает финишный экран с результатами гонки.

        Вычисляет время заезда, среднюю скорость, начисляет очки пользователю
        и отображает всю информацию на экране.

        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки.
            width (int): Ширина экрана.
            height (int): Высота экрана.
            time_start_race (datetime.datetime): Время начала гонки.
            speeds (list): Список зафиксированных скоростей.
            count_lose_shift (int): Количество неудачных переключений.
            user: Объект пользователя.
        """
        time_end_race = datetime.datetime.now()
        time_spend = (time_end_race - time_start_race).total_seconds()
        speed_average = sum(speeds) / len(speeds) if speeds else 0

        if is_false_start != True:
            user_score = user.set_user_score(time_spend, speed_average, count_lose_shift)

        font_small = WindowPattern().get_font("small")
        text_color_simple = WindowPattern().get_text_colors("simple")
        text_color_success = WindowPattern().get_text_colors("success")
        text_color_unsuccess = WindowPattern().get_text_colors("unsuccess")

        screen_color = WindowPattern().get_screen_color()

        pygame.draw.rect(screen, screen_color, (width / 4, height / 4, 400, 300), border_radius=25)
        pygame.draw.rect(screen, (0, 0, 0), (width / 4, height / 4, 400, 300), border_radius=25, width=2)

        text_finish = font_small.render("!ГОНКА ЗАВЕРШЕНА!", True, text_color_success)
        text_time_spend = font_small.render(f"Время заезда {round(time_spend, 2)} секунд", True, text_color_simple)
        text_speed_average = font_small.render(f"Средняя скорость {round(speed_average, 2)} км/ч", True,
                                               text_color_simple)
        if is_false_start == True:
            text_user_score = font_small.render(f"Заработано 0 очков. (!Фальстарт!)", True, text_color_unsuccess)
        else:
            text_user_score = font_small.render(f"Заработано {user_score} очков", True, text_color_simple)

        text_last_best_statistics = font_small.render('Последние результаты на машине:', True, text_color_simple)
        text_last_best_statistics_time = font_small.render(f'Время: {user.data[car.title].get('best_time')}', True, text_color_simple)

        if is_false_start != True:
            user.set_statistic_races(car_name=car.title, spend_time=round(time_spend, 2))

        screen.blit(text_finish, ((width / 4) + 85, (height / 4) + 20))
        screen.blit(text_time_spend, ((width / 4) + 35, (height / 4) + 70))
        screen.blit(text_speed_average, ((width / 4) + 35, (height / 4) + 130))
        screen.blit(text_user_score, ((width / 4) + 35, (height / 4) + 180))
        screen.blit(text_last_best_statistics, ((width / 4) + 35, (height / 4) + 230))
        screen.blit(text_last_best_statistics_time, ((width / 4) + 35, (height / 4) + 260))
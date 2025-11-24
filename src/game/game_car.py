"""
Модуль для симуляции автомобилей и их двигателей в игре Pygame.

Содержит классы Car и Engine для моделирования физики автомобиля,
переключения передач и управления оборотами двигателя.
"""

import pygame
import math
import datetime
import json

from src.utils.utils_paths import Utils


class Car(pygame.sprite.Sprite):
    """
    Класс автомобиля, наследующий pygame.sprite.Sprite.

    Управляет характеристиками автомобиля, его изображением, двигателем
    и логикой переключения передач с учетом буста.

    Attributes:
        name (str): Идентификатор автомобиля для загрузки конфигурации.
        current_gear (int): Текущая передача автомобиля.
        engine (Engine): Экземпляр двигателя автомобиля.
        speed (float): Текущая скорость автомобиля.
        boost_frames_remaining (int): Количество кадров, оставшихся для буста.
    """

    def __init__(self, name):
        """
        Инициализирует автомобиль с заданным именем.

        Args:
            name (str): Идентификатор автомобиля для загрузки конфигурации.

        Raises:
            ValueError: Если не удается загрузить характеристики или изображение.
        """
        super().__init__()
        self.name = name
        self.current_gear = 0
        self._load_assets()

        self.engine = Engine(
            self.get_gap_to_boost(),
            self.dict_gear_ratio_pair,
            self.time_max_throttle,
            self.wheel_circle,
            self.min_revolutions,
            self.max_revolutions
        )
        self.max_speed = self.get_max_speed()
        self._load_image(0)
        self.speed = 0

        self.boost_frames_remaining = 0

    def _load_assets(self):
        """
        Загружает характеристики автомобиля из JSON-файла.

        Читает конфигурационный файл car_{name}.json и инициализирует
        все атрибуты автомобиля из этого файла.

        Raises:
            ValueError: Если не удается загрузить или распарсить JSON-файл.
        """
        try:
            with open(Utils().get_asset_path('cars', f'car_{self.name}.json'), 'r', encoding='utf-8') as asset_car:
                data = json.load(asset_car)
                self.first_image = data['image']
                self.title = data['name']
                self.car_class = data['class']
                self.animation = data["animation"]
                self.score_to_unlocking = data['score_to_unlocking']
                self.horse_power = data['horse_power']
                self.scale = data['scale']
                self.coordinate_x = data['coordinate_x']
                self.coordinate_y = data['coordinate_y']
                self.dict_gear_ratio_pair = data['dict_gear_ratio_pair']
                self.time_max_throttle = data['time_max_throttle']
                self.frames_after_shift = data['frames_after_shift']
                self.wheel_circle = data['wheel_circle']
                self.min_revolutions = data['min_revolutions']
                self.max_revolutions = data['max_revolutions']
        except Exception as e:
            print(f"Ошибка загрузки машины '{self.name}': {type(e).__name__}: {e}")
            raise ValueError(f"Характеристики машины '{self.name}' не были загружены. "
                             f"Ошибка: {e}")

    def _load_image(self, state):
        """
        Загружает и масштабирует изображение автомобиля.

        Создает pygame Surface из файла изображения, применяет масштабирование
        и устанавливает начальную позицию спрайта.

        Raises:
            ValueError: Если не удается загрузить файл изображения.
        """
        try:
            self.original_image = pygame.image.load(
                Utils().get_resource_path('images', 'cars',f'car_{self.name}', f'car_{self.name}_state{state}.png')
            ).convert_alpha()
            if self.scale != 1.0:
                new_size = (
                    int(self.original_image.get_width() * self.scale),
                    int(self.original_image.get_height() * self.scale)
                )
                self.original_image = pygame.transform.scale(self.original_image, new_size)
            self.image = self.original_image
            self.rect = self.image.get_rect()
            self.rect.x = self.coordinate_x
            self.rect.y = self.coordinate_y
        except Exception as e:
            print(f"Ошибка загрузки изображения машины '{self.first_image}': {type(e).__name__}: {e}")
            raise ValueError(f"Изображение машины '{self.first_image}' не было загружено. "
                             f"Ошибка: {e}")

    def get_gap_to_boost(self):
        """
        Возвращает диапазон оборотов для активации буста в зависимости от класса автомобиля.

        Returns:
            int: Размер диапазона оборотов для буста (600 для low, 400 для sport, 300 для остальных).
        """
        if self.car_class == "low":
            return 600
        elif self.car_class == "sport":
            return 400
        else:
            return 300

    def get_max_speed(self):
        """
        Вычисляет максимальную скорость автомобиля на последней передаче.

        Returns:
            int: Максимальная скорость в км/ч, округленная вверх.
        """
        last_gear = max(int(k) for k in self.dict_gear_ratio_pair if k.isdigit() and int(k) > 0)
        max_speed = math.ceil(
            (self.max_revolutions * self.wheel_circle * 60)
            / (self.dict_gear_ratio_pair["main"] * self.dict_gear_ratio_pair[str(last_gear)] * 1000)
        )
        return max_speed

    def update(self, is_good_shift):
        """
        Обновляет состояние автомобиля на каждом кадре.

        Обновляет обороты двигателя, вычисляет текущую скорость с учетом буста
        и применяет штрафы за плохое переключение передачи.

        Args:
            is_good_shift (bool): True, если последнее переключение было хорошим.
        """
        self.engine.update_throttle()
        base_speed = self.engine.get_current_speed() * 0.2778 * 2

        if self.boost_frames_remaining > 0:
            self.speed = base_speed * 1.5
            self.boost_frames_remaining -= 1
        else:
            self.speed = base_speed

        if not is_good_shift:
            self.speed *= 0.5
            self.engine.throttle *= 0.5
            self.engine.acceleration_progress *= 0.5
            self.boost_frames_remaining = 0

    def start_engine(self):
        """
        Запускает ускорение двигателя.

        Инициирует процесс набора оборотов двигателя.
        """
        self.engine.start_acceleration()

    def shift_gear(self, new_gear):
        """
        Переключает передачу и определяет качество переключения.

        Проверяет, было ли переключение выполнено в зоне буста, и активирует
        буст на 60 кадров при успешном переключении.

        Args:
            new_gear (int): Номер новой передачи.

        Returns:
            bool: True, если переключение было выполнено корректно.
        """
        is_boost_shift = self.engine.is_boost()

        self.engine.shift_gear(new_gear)
        self.current_gear = new_gear

        is_good = self.engine.is_good_shift(new_gear)

        if is_boost_shift and is_good:
            self.boost_frames_remaining = 60

        return is_good

    def get_engine_info(self):
        """
        Возвращает текущую информацию о состоянии двигателя.

        Returns:
            dict: Словарь с ключами 'rpm', 'gear', 'speed_kmh', 'throttle'.
        """
        return {
            'rpm': self.engine.revolutions,
            'gear': self.current_gear,
            'speed_kmh': self.engine.get_current_speed(),
            'throttle': self.engine.throttle
        }


class Engine:
    """
    Класс двигателя автомобиля.

    Моделирует работу двигателя: обороты, дроссель, переключение передач,
    расчет скорости и определение зон для буста и корректных переключений.

    Attributes:
        current_gear (int): Текущая передача.
        revolutions (float): Текущие обороты двигателя (об/мин).
        throttle (float): Уровень открытия дросселя (0.0-1.0).
        acceleration_progress (float): Прогресс ускорения (0.0-1.0).
    """

    def __init__(self, gap_to_boost, dict_gear_ratio_pair, time_max_throttle,
                 wheel_circle, min_revolutions, max_revolutions):
        """
        Инициализирует двигатель с заданными параметрами.

        Args:
            gap_to_boost (int): Размер диапазона оборотов для буста.
            dict_gear_ratio_pair (dict): Словарь передаточных чисел.
            time_max_throttle (dict): Словарь времени разгона на каждой передаче.
            wheel_circle (float): Длина окружности колеса в метрах.
            min_revolutions (int): Минимальные обороты двигателя.
            max_revolutions (int): Максимальные обороты двигателя.
        """
        self.current_gear = 0
        self._dict_gear_ratio_pair = dict_gear_ratio_pair
        self._time_max_throttle = time_max_throttle
        self._wheel_circle = wheel_circle

        self.min_revolutions = min_revolutions
        self.min_revolutions_to_good_shift = self.min_revolutions * 2

        self.max_revolutions = max_revolutions
        self.max_revolutions_to_good_shift = self.max_revolutions - gap_to_boost

        self.max_revolutions_to_boost = self.max_revolutions_to_good_shift - gap_to_boost
        self.min_revolutions_to_boost = self.max_revolutions_to_boost - gap_to_boost

        self.revolutions = self.min_revolutions
        self.throttle = 0.0
        self.start_time = None
        self.acceleration_progress = 0.0
        self.count_gear = len(self._dict_gear_ratio_pair) - 2

        self.gear_ratio_main_pair = self._dict_gear_ratio_pair["main"]
        self.gear_ratio_current_pair = self._dict_gear_ratio_pair[str(self.current_gear)]

    def start_acceleration(self):
        """
        Начинает процесс ускорения двигателя.

        Устанавливает начальное время для расчета прогресса ускорения.
        """
        self.start_time = datetime.datetime.now()

    def update_throttle(self):
        """
        Обновляет уровень дросселя и обороты двигателя.

        Вычисляет прогресс ускорения на основе прошедшего времени
        и обновляет текущие обороты двигателя.
        """
        if self.start_time is not None:
            current_time = datetime.datetime.now()
            elapsed = (current_time - self.start_time).total_seconds()
            total_time = self._time_max_throttle[str(self.current_gear)]

            if total_time == 0:
                self.throttle = 0
                self.acceleration_progress = 0
            else:
                new_progress = min(self.acceleration_progress + (elapsed / total_time), 1.0)
                self.acceleration_progress = new_progress
                self.throttle = new_progress

            self.revolutions = self.min_revolutions + (
                    self.throttle * (self.max_revolutions - self.min_revolutions)
            )

            self.start_time = current_time

    def shift_gear(self, new_gear):
        """
        Переключает передачу и сбрасывает прогресс ускорения.

        При переключении сохраняется 60% текущего прогресса ускорения,
        обновляется передаточное число и перезапускается таймер.

        Args:
            new_gear (int): Номер новой передачи.
        """
        self.acceleration_progress = self.throttle * 0.6
        self.current_gear = new_gear  # ИСПРАВЛЕНИЕ: переименовано с current_broadcast
        self.gear_ratio_current_pair = self._dict_gear_ratio_pair[str(new_gear)]
        self.start_time = datetime.datetime.now()

    def get_current_speed(self):
        """
        Вычисляет текущую скорость автомобиля в км/ч.

        Использует текущие обороты, передаточные числа и длину окружности колеса
        для расчета скорости.

        Returns:
            int: Текущая скорость в км/ч, округленная вверх.
        """
        if self.gear_ratio_current_pair == 0 or self.current_gear == 0:
            return 0
        else:
            return math.ceil(
                (self.revolutions * self._wheel_circle * 60)
                / (self.gear_ratio_main_pair * self.gear_ratio_current_pair * 1000)
            )

    def calculate_rpm_after_shift(self, new_gear):
        """
        Вычисляет обороты двигателя после переключения передачи.

        Рассчитывает, какими будут обороты после переключения на новую передачу
        на основе текущих оборотов и передаточных чисел.

        Args:
            new_gear (int): Номер новой передачи.

        Returns:
            float: Прогнозируемые обороты после переключения.
        """
        if self.current_gear == 0 or new_gear == 0:
            return self.min_revolutions

        current_ratio = self._dict_gear_ratio_pair[
            str(self.current_gear)]
        new_ratio = self._dict_gear_ratio_pair[str(new_gear)]

        rpm_after = self.revolutions * (new_ratio / current_ratio)
        rpm_after = max(self.min_revolutions, rpm_after)

        return rpm_after

    def is_good_shift(self, new_gear):
        """
        Проверяет, было ли переключение передачи выполнено корректно.

        Переключение считается корректным, если прогнозируемые обороты после
        переключения попадают в допустимый диапазон.

        Args:
            new_gear (int): Номер новой передачи.

        Returns:
            bool: True, если переключение корректное; False в противном случае.
        """
        rpm_after = self.calculate_rpm_after_shift(new_gear)
        if new_gear != 1:
            return self.min_revolutions_to_good_shift <= rpm_after <= self.max_revolutions_to_good_shift
        else:
            return True

    def is_boost(self):
        """
        Проверяет, находятся ли текущие обороты в зоне буста.

        Returns:
            bool: True, если обороты в зоне буста; False в противном случае.
        """
        return self.min_revolutions_to_boost <= self.revolutions <= self.max_revolutions_to_boost

import pygame
import math
import datetime
import json

from src.utils.utils_paths import Utils

class Car(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self.current_gear = 0
        self._load_assets()

        self.engine = Engine(self.get_gap_to_boost(), self.dict_gear_ratio_pair, self.time_max_throttle, self.wheel_circle,
                             self.min_revolutions, self.max_revolutions)
        self.max_speed = self.get_max_speed()
        self._load_image()
        self.speed = 0

        self.boost_frames_remaining = 0

    def _load_assets(self):
        try:
            with open(Utils().get_asset_path('cars',f'car_{self._name}.json'), 'r', encoding='utf-8') as asset_car:
                data = json.load(asset_car)
                self.first_image = data['image']
                self.name = data['name']
                self.car_class = data['class']
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
        except:
            raise ValueError("Характеристики машины не были загружены. Проверьте файл конфигурации автомобиля.")

    def _load_image(self):
        try:
            self.original_image = pygame.image.load(Utils().get_resource_path('images', 'cars', self.first_image)).convert_alpha()
            if self.scale != 1.0:
                new_size = (int(self.original_image.get_width() * self.scale),
                            int(self.original_image.get_height() * self.scale))
                self.original_image = pygame.transform.scale(self.original_image, new_size)
            self.image = self.original_image
            self.rect = self.image.get_rect()
            self.rect.x = self.coordinate_x
            self.rect.y = self.coordinate_y
        except:
            raise ValueError("Изображение машины не были загружены. Проверьте путь к файлу.")

    def get_gap_to_boost(self):
        if self.car_class == "low":
            return 600
        elif self.car_class == "sport":
            return 400
        else:
            return 300

    def get_max_speed(self):
        last_gear = max(int(k) for k in self.dict_gear_ratio_pair if k.isdigit() and int(k) > 0)
        max_speed = math.ceil((self.max_revolutions * self.wheel_circle * 60)
                                   / (self.dict_gear_ratio_pair["main"] * self.dict_gear_ratio_pair[str(last_gear)] * 1000))
        return max_speed

    def update(self, is_good_shift):
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
        self.engine.start_acceleration()

    def shift_gear(self, new_gear):
        is_boost_shift = self.engine.is_boost()

        self.engine.shift_gear(new_gear)
        self.current_gear = new_gear

        is_good = self.engine.is_good_shift(new_gear)

        if is_boost_shift and is_good:
            self.boost_frames_remaining = 60

        return is_good

    def get_engine_info(self):
        return {
            'rpm': self.engine.revolutions,
            'gear': self.current_gear,
            'speed_kmh': self.engine.get_current_speed(),
            'throttle': self.engine.throttle
        }


class Engine:
    def __init__(self, gap_to_boost, dict_gear_ratio_pair, time_max_throttle, wheel_circle, min_revolutions, max_revolutions):
        self.current_broadcast = 0
        self._dict_gear_ratio_pair = dict_gear_ratio_pair
        self._time_max_throttle = time_max_throttle
        self._wheel_circle = wheel_circle

        self.min_revolutions = min_revolutions
        self.min_revolutions_to_good_shift = self.min_revolutions * 2

        self.max_revolutions = max_revolutions
        self.max_revolutions_to_good_shift = self.max_revolutions - self.min_revolutions

        self.max_revolutions_to_boost = self.max_revolutions_to_good_shift - gap_to_boost
        self.min_revolutions_to_boost = self.max_revolutions_to_boost - gap_to_boost


        self.revolutions = self.min_revolutions
        self.throttle = 0.0
        self.start_time = None
        self.acceleration_progress = 0.0
        self.count_gear = len(self._dict_gear_ratio_pair) - 2

        self.gear_ratio_main_pair = self._dict_gear_ratio_pair["main"]
        self.gear_ratio_current_pair = self._dict_gear_ratio_pair[str(self.current_broadcast)]

    def start_acceleration(self):
        self.start_time = datetime.datetime.now()

    def update_throttle(self):
        if self.start_time is not None:
            current_time = datetime.datetime.now()
            elapsed = (current_time - self.start_time).total_seconds()
            total_time = self._time_max_throttle[str(self.current_broadcast)]

            if total_time == 0:
                self.throttle = 0
            else:
                new_progress = min(self.acceleration_progress + (elapsed / total_time), 1.0)
                self.throttle = new_progress

            self.revolutions = self.min_revolutions + (self.throttle * (self.max_revolutions - self.min_revolutions))

    def shift_gear(self, new_gear):
        self.acceleration_progress = self.throttle * 0.6
        self.current_broadcast = new_gear
        self.gear_ratio_current_pair = self._dict_gear_ratio_pair[str(new_gear)]
        self.start_time = datetime.datetime.now()

    def get_current_speed(self):
        if self.gear_ratio_current_pair == 0 or self.current_broadcast == 0:
            return 0
        else:
            return math.ceil((self.revolutions * self._wheel_circle * 60)
                             / (self.gear_ratio_main_pair * self.gear_ratio_current_pair * 1000))

    def calculate_rpm_after_shift(self, new_gear):
        if self.current_broadcast == 0 or new_gear == 0:
            return self.min_revolutions

        current_ratio = self._dict_gear_ratio_pair[str(self.current_broadcast)]
        new_ratio = self._dict_gear_ratio_pair[str(new_gear)]

        rpm_after = self.revolutions * (new_ratio / current_ratio)
        rpm_after = max(self.min_revolutions, rpm_after)

        return rpm_after

    def is_good_shift(self, new_gear):
        rpm_after = self.calculate_rpm_after_shift(new_gear)
        if new_gear != 1:
            return self.min_revolutions_to_good_shift < rpm_after < self.max_revolutions_to_good_shift
        else:
            return True

    def is_boost(self):
        return self.min_revolutions_to_boost < self.revolutions < self.max_revolutions_to_boost

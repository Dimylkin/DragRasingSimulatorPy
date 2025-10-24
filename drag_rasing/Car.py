import pygame
import math
import datetime
import time
import json

class Car(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.current_gear = 0
        self.load_ttx()
        self.load_image()
        self.speed = 0
        self.engine = Engine(self)

    def load_ttx(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as car_ttx:
                data = json.load(car_ttx)
                self.image = data['image']
                self.scale = data['scale']
                self.coordinate_x = data['coordinate_x']
                self.coordinate_y = data['coordinate_y']
                self.dict_gear_ratio_pair = data['dict_gear_ratio_pair']
                self.time_max_throttle = data['time_max_throttle']
                self.wheel_circle = data['wheel_circle']
                self.min_revolutions = data['min_revolutions']
                self.max_revolutions = data['max_revolutions']
        except:
            raise ValueError("Характеристики машины не были загружены. Проверьте файл конфигурации автомобиля.")

    def load_image(self):
        try:
            self.original_image = pygame.image.load(self.image).convert_alpha()
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

    def update(self, is_good_shift):
        self.engine.update_throttle()
        self.speed = self.engine.get_current_speed() * 0.2778 * 2
        if is_good_shift != True:
            self.speed *= 0.5
            self.engine.throttle *= 0.5
            self.engine.acceleration_progress *= 0.5

    def start_engine(self):
        self.engine.start_acceleration()

    def shift_gear(self, new_gear):
        self.engine.shift_gear(new_gear)
        self.current_gear = new_gear

        if self.engine.is_good_shift(new_gear):
            return True
        else:
            return False

    def get_engine_info(self):
        return {
            'rpm': self.engine.revolutions,
            'gear': self.current_gear,
            'speed_kmh': self.engine.get_current_speed(),
            'throttle': self.engine.throttle
        }

class Bot(Car, pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.level = level
        if level == "Low":
            self.name = "vaz_2101"
        elif level == "Middle":
            self.name = "audi_rs6"
        else:
            pass
            #self.name = lamborghini_murcielago
        Car(self.name)


class Engine:
    def __init__(self, car):
        self.current_broadcast = 0
        self.car = car
        self.dict_gear_ratio_pair = car.dict_gear_ratio_pair
        self.time_max_throttle = car.time_max_throttle
        self.wheel_circle = car.wheel_circle
        self.min_revolutions = car.min_revolutions
        self.max_revolutions = car.max_revolutions
        self.revolutions = self.min_revolutions
        self.throttle = 0.0
        self.start_time = None
        self.acceleration_progress = 0.0
        self.count_gear = len(self.dict_gear_ratio_pair) - 2

        self.gear_ratio_main_pair = self.dict_gear_ratio_pair["main"]
        self.gear_ratio_current_pair = self.dict_gear_ratio_pair[str(self.current_broadcast)]

    def start_acceleration(self):
        self.start_time = datetime.datetime.now()

    def update_throttle(self):
        if self.start_time is not None:
            current_time = datetime.datetime.now()
            elapsed = (current_time - self.start_time).total_seconds()
            total_time = self.time_max_throttle[str(self.current_broadcast)]

            if total_time == 0:
                self.throttle = 0
            else:
                new_progress = min(self.acceleration_progress + (elapsed / total_time), 1.0)
                self.throttle = new_progress

            self.revolutions = self.min_revolutions + (self.throttle * (self.max_revolutions - self.min_revolutions))

    def shift_gear(self, new_gear):
        self.acceleration_progress = self.throttle * 0.6
        self.current_broadcast = new_gear
        self.gear_ratio_current_pair = self.dict_gear_ratio_pair[str(new_gear)]
        self.start_time = datetime.datetime.now()

    def get_current_speed(self):
        if self.gear_ratio_current_pair == 0 or self.current_broadcast == 0:
            return 0
        else:
            return math.ceil((self.revolutions * self.wheel_circle * 60)
                             / (self.gear_ratio_main_pair * self.gear_ratio_current_pair * 1000))

    def calculate_rpm_after_shift(self, new_gear):
        if self.current_broadcast == 0 or new_gear == 0:
            return min_revolutions

        current_ratio = self.dict_gear_ratio_pair[str(self.current_broadcast)]
        new_ratio = self.dict_gear_ratio_pair[str(new_gear)]

        rpm_after = self.revolutions * (new_ratio / current_ratio)
        rpm_after = max(self.min_revolutions, rpm_after)

        return rpm_after

    def is_good_shift(self, new_gear):
        rpm_after = self.calculate_rpm_after_shift(new_gear)
        if rpm_after < self.min_revolutions + self.min_revolutions or rpm_after > self.max_revolutions - self.min_revolutions:
            return False
        else:
            return True
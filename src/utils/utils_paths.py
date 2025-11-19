"""
Модуль утилит для работы с путями и ресурсами.

Содержит класс Utils для управления путями к ресурсам приложения,
получения списков пользователей, треков и автомобилей.
"""

import os


class Utils:
    """
    Класс утилит для работы с путями и ресурсами приложения.

    Предоставляет методы для получения абсолютных путей к ресурсам,
    конфигурационным файлам и спискам доступных элементов игры.

    Attributes:
        base_path (str): Базовый путь к корневой директории проекта.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """
        Создает единственный экземпляр класса (Singleton).

        Returns:
            Utils: Единственный экземпляр класса.
        """
        if cls._instance is None:
            cls._instance = super(Utils, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Инициализирует утилиты путей.

        Вычисляет базовый путь к корневой директории проекта.
        """
        if Utils._initialized:
            return

        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        Utils._initialized = True

    def get_resource_path(self, *path):
        """
        Возвращает абсолютный путь к ресурсу в директории resources.

        Args:
            *path: Компоненты пути относительно директории resources.

        Returns:
            str: Абсолютный путь к ресурсу.

        Example:
            >>> utils = Utils()
            >>> utils.get_resource_path('images', 'cars', 'car1.png')
            '/path/to/project/resources/images/cars/car1.png'
        """
        return os.path.join(self.base_path, 'resources', *path)

    def get_asset_path(self, *path):
        """
        Возвращает абсолютный путь к ресурсу в директории assets.

        Args:
            *path: Компоненты пути относительно директории assets.

        Returns:
            str: Абсолютный путь к ресурсу.

        Example:
            >>> utils = Utils()
            >>> utils.get_asset_path('users', 'user_player1.json')
            '/path/to/project/assets/users/user_player1.json'
        """
        return os.path.join(self.base_path, 'assets', *path)

    def get_list_users(self):
        """
        Возвращает список идентификаторов пользователей.

        Сканирует директорию assets/users и извлекает идентификаторы
        из имен файлов формата 'user_{id}.json'.

        Returns:
            list: Список идентификаторов пользователей.

        Raises:
            FileNotFoundError: Если директория пользователей не найдена.
        """
        try:
            users_path = self.get_asset_path('users')
            list_users = []
            for file in os.listdir(users_path):
                if file.startswith('user_') and file.endswith('.json'):
                    user = file[5:-5]
                    list_users.append(user)
            return list_users
        except FileNotFoundError as e:
            print(f"Ошибка: директория пользователей не найдена: {e}")
            return []

    def get_list_tracks(self):
        """
        Возвращает список идентификаторов треков.

        Сканирует директорию resources/images/tracks и извлекает идентификаторы
        из имен файлов формата 'track_{id}.png'.

        Returns:
            list: Список идентификаторов треков.

        Raises:
            FileNotFoundError: Если директория треков не найдена.
        """
        try:
            tracks_path = self.get_resource_path('images', 'tracks')
            list_tracks = []
            for file in os.listdir(tracks_path):
                if file.startswith('track_') and file.endswith('.png'):
                    track = file[6:-4]
                    list_tracks.append(track)
            return list_tracks
        except FileNotFoundError as e:
            print(f"Ошибка: директория треков не найдена: {e}")
            return []

    def get_list_cars(self):
        """
        Возвращает список идентификаторов автомобилей.

        Сканирует директорию resources/images/cars и извлекает идентификаторы
        из имен файлов формата 'car_{id}.png'.

        Returns:
            list: Список идентификаторов автомобилей.

        Raises:
            FileNotFoundError: Если директория автомобилей не найдена.
        """
        try:
            cars_path = self.get_resource_path('images', 'cars')
            list_cars = []
            for file in os.listdir(cars_path):
                if file.startswith('car_') and file.endswith('.png'):
                    car = file[4:-4]
                    list_cars.append(car)
            return list_cars
        except FileNotFoundError as e:
            print(f"Ошибка: директория автомобилей не найдена: {e}")
            return []

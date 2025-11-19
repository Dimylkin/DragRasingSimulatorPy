"""
Модуль для управления пользователями в игре.

Содержит класс User для хранения информации о пользователе,
расчета и обновления игрового счета.
"""

from src.utils.utils_paths import Utils
import json


class User:
    """
    Класс пользователя игры.

    Управляет информацией о пользователе, включая никнейм, изображение и счет.
    Позволяет загружать данные пользователя из JSON-файла и обновлять счет
    на основе результатов игры.

    Attributes:
        name (str): Идентификатор пользователя для загрузки конфигурации.
        nickname (str): Отображаемое имя пользователя.
        image (str): Путь к изображению профиля пользователя.
        score (int): Текущий игровой счет пользователя.
    """

    def __init__(self, name):
        """
        Инициализирует пользователя с заданным идентификатором.

        Args:
            name (str): Идентификатор пользователя для загрузки конфигурации.

        Raises:
            ValueError: Если не удается загрузить данные пользователя.
        """
        self.name = name
        self._load_resources(self.name)

    def _load_resources(self, name):
        """
        Загружает данные пользователя из JSON-файла.

        Читает конфигурационный файл user_{name}.json и инициализирует
        атрибуты пользователя: никнейм, изображение и счет.

        Args:
            name (str): Идентификатор пользователя.

        Raises:
            FileNotFoundError: Если файл пользователя не найден.
            json.JSONDecodeError: Если JSON-файл имеет неверный формат.
            KeyError: Если в JSON отсутствуют необходимые ключи.
        """
        try:
            with open(Utils().get_asset_path('users', f'user_{name}.json'), 'r', encoding='utf-8') as asset_user:
                data = json.load(asset_user)
                self.nickname = data['name']
                self.image = data['image']
                self.score = data['score']
        except FileNotFoundError:
            print(f"Ошибка: файл пользователя '{name}' не найден.")
            raise ValueError(f"Файл пользователя '{name}' не существует.")
        except json.JSONDecodeError as e:
            print(f"Ошибка: неверный формат JSON для пользователя '{name}': {e}")
            raise ValueError(f"Некорректный JSON-файл пользователя '{name}'.")
        except KeyError as e:
            print(f"Ошибка: отсутствует ключ {e} в данных пользователя '{name}'.")
            raise ValueError(f"Неполные данные пользователя '{name}': отсутствует ключ {e}.")

    def set_user_score(self, time_spend, speed_average, lose_shift_count):
        """
        Вычисляет и обновляет счет пользователя на основе результатов игры.

        Формула расчета очков:
        score = round(100 + 20 * (10 / time_spend) + 100 * speed_average - 5 * lose_shift_count)

        Вычисленный счет добавляется к текущему счету пользователя,
        и обновленное значение сохраняется в JSON-файл.

        Args:
            time_spend (float): Время, затраченное на прохождение (в секундах). Должно быть > 0.
            speed_average (float): Средняя скорость во время игры (в км/ч). Должна быть > 0.
            lose_shift_count (int): Количество неудачных переключений передач.

        Returns:
            int: Количество очков, добавленных к счету пользователя.

        Raises:
            ValueError: Если time_spend или speed_average <= 0.
            FileNotFoundError: Если файл пользователя не найден при сохранении.
            json.JSONDecodeError: Если JSON-файл имеет неверный формат при чтении.
            IOError: Если возникла ошибка при записи в файл.
        """
        if time_spend <= 0:
            raise ValueError(f"time_spend должно быть больше 0, получено: {time_spend}")
        if speed_average <= 0:
            raise ValueError(f"speed_average должна быть больше 0, получено: {speed_average}")

        score = round(100 + 20 * (10 / time_spend) + 100 * speed_average - 5 * lose_shift_count)
        self.score += score

        file_path = Utils().get_asset_path('users', f'user_{self.name}.json')

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            data['score'] = self.score

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)

        except FileNotFoundError:
            print(f"Ошибка: файл пользователя '{self.name}' не найден при сохранении.")
            raise
        except json.JSONDecodeError as e:
            print(f"Ошибка: неверный формат JSON при чтении файла '{self.name}': {e}")
            raise
        except IOError as e:
            print(f"Ошибка ввода-вывода при работе с файлом пользователя '{self.name}': {e}")
            raise

        return score

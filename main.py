"""
Главный модуль запуска приложения Драг Рейсинг.

Инициализирует пользователя и запускает стартовое окно игры.
"""

from src.ui.windows.window_start import WindowStart
from src.game.game_user import User


def main():
    """
    Главная функция запуска приложения.

    Создает объект пользователя и запускает главное окно игры.
    Обрабатывает исключения для корректного завершения при ошибках.
    """
    try:
        user = User("ivan")
        start = WindowStart(user)
        start.run()
    except Exception as e:
        print(f"Критическая ошибка при запуске приложения: {e}")
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()

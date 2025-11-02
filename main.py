from src.ui.windows.window_start import WindowStart
from src.game.game_user import User

if __name__ == "__main__":
    user = User("admin")
    start = WindowStart(user)
    start.run()
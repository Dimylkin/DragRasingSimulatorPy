from src.utils.utils_paths import Utils
import json


class User:
    def __init__(self, name):
        self.name = name
        self._load_resources(self.name)


    def _load_resources(self, name):
        with open(Utils().get_asset_path('users', f'user_{name}.json'), 'r', encoding='utf-8') as asset_user:
            data = json.load(asset_user)
            self.nickname = data['name']
            self.image = data['image']
            self.score = data['score']

    def set_user_score(self, time_spend, speed_average, lose_shift_count):
        score = round(100 + 20 * (10 / time_spend) + 100 / speed_average - 5 * lose_shift_count)
        self.score += score

        file_path = Utils().get_asset_path('users', f'user_{self.name}.json')

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        data['score'] = self.score

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        return score

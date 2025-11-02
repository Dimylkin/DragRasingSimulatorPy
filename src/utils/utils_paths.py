import os


class Utils:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.list_maps = self.get_list_tracks()
        self.list_cars = self.get_list_cars()

    def get_resource_path(self, *path):
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(self.base_path, 'resources', *path)

    def get_asset_path(self, *path):
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(self.base_path, 'assets', *path)

    def get_list_users(self):
        list_users = []
        for file in os.listdir(self.get_asset_path('users')):
            user = file[5:][:-5]
            list_users.append(user)
        return list_users

    def get_list_tracks(self):
        list_tracks = []
        for file in os.listdir(self.get_resource_path('images', 'tracks')):
            track = file[6:][:-4]
            list_tracks.append(track)
        return list_tracks

    def get_list_cars(self):
        list_cars = []
        for file in os.listdir(self.get_resource_path('images', 'cars')):
            car = file[4:][:-4]
            list_cars.append(car)
        return list_cars
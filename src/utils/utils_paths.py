import os

def get_resource_path(*path):
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_path, 'resources', *path)

def get_asset_path(*path):
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_path, 'assets', *path)
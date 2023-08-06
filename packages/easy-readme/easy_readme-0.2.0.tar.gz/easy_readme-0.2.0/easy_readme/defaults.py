import os


def get_default_project_name(path):
    path_pieces = os.path.split(path)
    current_directory = path_pieces[-1]
    current_directory = current_directory.replace('-', ' ')
    current_directory = current_directory.replace('_', ' ')
    return current_directory.title()

import os

from engine_utils.directory_info import DirectoryInfo


def validate_search_path(search_path):
    if not os.path.isabs(search_path):
        if os.path.isdir(search_path):
            search_path = os.path.abspath(search_path)
        else:
            search_path = os.path.join(DirectoryInfo.get_project_dir(), search_path)
    if not os.path.isdir(search_path):
        return None
    if not os.path.isabs(search_path):
        search_path = os.path.abspath(search_path)
    return search_path

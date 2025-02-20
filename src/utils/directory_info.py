import os


class DirectoryInfo(object):
    file_path = __file__
    utils_dir = os.path.dirname(file_path)
    src_dir = os.path.dirname(utils_dir)
    project_dir = os.path.dirname(src_dir)

    @classmethod
    def get_project_dir(cls):
        return cls.project_dir

    @classmethod
    def get_src_dir(cls):
        return cls.src_dir

    @classmethod
    def get_log_dir(cls):
        return os.path.join(cls.project_dir, 'log')

    @classmethod
    def get_config_dir(cls):
        return os.path.join(cls.project_dir, 'config')

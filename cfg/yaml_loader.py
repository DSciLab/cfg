import os
import yaml


class YAMLLoader(object):
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            self.cfg = self.load_yaml(file_path)
        self.import_cfg()

    def load_yaml(self, file_path):
        with open(file_path, 'r') as f:
            return yaml.load(f, yaml.FullLoader)

    @staticmethod
    def auto_file_ext(root_path, file_path):
        ext = root_path.split('.')[-1]
        file_path_dot_splited = file_path.split('.')
        if len(file_path_dot_splited) == 0 or \
            file_path_dot_splited[-1] not in ['yml', 'yaml']:
            return file_path + f'.{ext}'
        return file_path

    @staticmethod
    def get_relative_path(root_path, file_path):
        # file.yaml
        # ./file.yaml
        # ../file.yaml
        # ../../file.yaml
        # ../path/file.yaml

        # drop `./` in the begining
        if file_path[:2] == './':
            file_path = file_path[2:]

        root_splited = root_path.split('/')
        sub_path_splited = file_path.split('../')

        root_splited = root_splited[:-len(sub_path_splited)]
        final_path_list = root_splited + sub_path_splited
        return os.path.join(*final_path_list)

    def import_cfg(self):
        import_files = self.cfg.get('import', [])
        if not isinstance(import_files, list):
            import_files = [import_files]
        import_files = reversed(import_files)

        for file in import_files:
            file = self.auto_file_ext(self.file_path, file)
            file = self.get_relative_path(self.file_path, file)
            sub_cfgs = self.load_yaml(file)
            sub_cfgs.update(self.cfg)
            self.cfg = sub_cfgs

    def __getitem__(self, key):
        return self.cfg[key]

    def get(self, key, default=None):
        return self.cfg.get(key, default)

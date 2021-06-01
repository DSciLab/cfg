import os
import yaml


class YAMLLoader(object):
    def load_yml(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            data = self._load_yaml(file_path)
        return data

    def _load_yaml(self, file_path):
        with open(file_path, 'r') as f:
            cfg = yaml.load(f, yaml.FullLoader)
        cfg = self.import_cfg(cfg)
        return cfg

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

    def import_cfg(self, curr_cfg):
        import_files = curr_cfg.get('import', [])
        if not isinstance(import_files, list):
            import_files = [import_files]
        import_files = reversed(import_files)

        for file in import_files:
            file = self.auto_file_ext(self.file_path, file)
            file = self.get_relative_path(self.file_path, file)
            sub_cfgs = self.load_yaml(file)
            if sub_cfgs:
                sub_cfgs.update(curr_cfg)
                curr_cfg = sub_cfgs
        return curr_cfg

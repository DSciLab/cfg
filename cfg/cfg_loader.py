from .yaml_loader import YAMLLoader
from .py_loader import PYLoader


class CFGLoader(YAMLLoader, PYLoader):
    def load_cfg(self, file_path: str) -> dict:
        assert '.' in file_path, f'file ({file_path}) has not extention.'

        file_ext = file_path.split('.')[-1]
        if file_ext in ('yml', 'yaml'):
            return self.load_yml(file_path)
        elif file_ext == 'py':
            return self.load_py(file_path)
        else:
            raise ValueError(f'Unrecognized file ({file_path}).')

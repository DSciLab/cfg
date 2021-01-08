import datetime
import yaml
from .yaml_loader import YAMLLoader
from .argparser import Args


class Opts(Args):
    def __init__(self, cfg_file=None, description=None, _parse_data=None):
        if cfg_file is not None:
            self._cfg = YAMLLoader(cfg_file).cfg
        else:
            self._cfg = {}
        self.add_with_dict(self._cfg)
        super().__init__(description)
        # _parse_data just for test
        self.parse(_parse_data)

        self._cfg.update(self.dict)
        self.try_load_registered_yml()
        self.post_config()
        self.set_attr()

    def try_load_registered_yml(self):
        _cfg = None
        for key, value in self._cfg.items():
            cfg_path = self.CFG_POOL.query(key, value)
            if cfg_path is not None:
                sub_cfg = YAMLLoader(cfg_path).cfg
                if _cfg is None:
                    _cfg = sub_cfg
                else:
                    _cfg.update(sub_cfg)
        self._cfg.update(_cfg)

    def post_config(self):
        if 'id' not in self._cfg:
            d = datetime.datetime.now()
            self._cfg['id'] = d.strftime('%Y%m%d_%H%M%S')

    def get(self, key, default=None):
        return self._cfg.get(key, default)

    def set(self, key, value):
        self._cfg[key] = value
        setattr(self, key, value)

    def __setattr__(self, key, value):
        if hasattr(self, '_cfg') and (len(key) < 2 or key[0] != '_'):
            self._cfg[key] = value
        return super().__setattr__(key, value)

    def set_attr(self):
        for k, v in self._cfg.items():
            setattr(self, k, v)

    def __getitem__(self, key):
        return self._cfg[key]
    
    def __setitem__(self, key, value):
        self.set(key, value)

    def dumps(self):
        return self._cfg

    def dump(self, file_path):
        # dump as yaml file
        with open(file_path, 'w') as f:
            data = self.dumps()
            yaml.dump(data, f)

    def load(self, file_path, update=True):
        with open(file_path, 'r') as f:
            cfg = yaml.load(f, yaml.FullLoader)
        self.loads(cfg, update)

    def loads(self, cfg, update=False):
        if update:
            cfg.update(self._cfg)
            self._cfg = cfg
        else:
            self._cfg = cfg
        self.set_attr()

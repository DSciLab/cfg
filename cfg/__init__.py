import datetime
import pickle
import yaml
import inspect
from .cfg_loader import CFGLoader
from .argparser import Args



class Opts(Args):
    def __init__(self, cfg_file=None, description=None, _parse_data=None):
        filename = inspect.stack()[1].filename
        if self.GROUP_NAME is None:
            filename = filename.split('/')[-1]
            group_name = filename.split('.')[0]
            self.GROUP_NAME = group_name
        if '.py' not in filename and _parse_data is None:
            _parse_data = ''
        
        if cfg_file is not None:
            self._cfg = CFGLoader().load_cfg(cfg_file)
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
        self.reset_class_var()

    @staticmethod
    def fix_relative_path(path, ref_path):
        splited_path = path.split('/')
        splited_ref_path = ref_path.split('/')
        final_splited_path = splited_ref_path[:-1] + splited_path
        final_path = '/'.join(final_splited_path)
        return final_path

    def init_pnp(self):
        for pnp_cfg_path in self.PNP_PATH_LIST:
            pnp_cfg = CFGLoader().load_cfg(pnp_cfg_path)
            for key in pnp_cfg.keys():
                pnp_item = pnp_cfg[key]
                assert isinstance(pnp_item, dict), \
                    'pnp configure file fomat error'
                for value, yaml_path in pnp_item.items():
                    if isinstance(yaml_path, str):
                        yaml_path_out = self.fix_relative_path(
                            yaml_path, pnp_cfg_path
                        )
                        yaml_path_out = [yaml_path_out]
                    else:
                        yaml_path_out = []
                        for yaml_path_ in yaml_path:
                            yaml_path_out.append(
                                self.fix_relative_path(
                                    yaml_path_, pnp_cfg_path
                                )
                            )

                    self.CFG_POOL.regist(key=key,
                                        value=value,
                                        cfg_path=yaml_path_out)

    def try_load_registered_yml(self):
        self.init_pnp()
        _cfg = None
        for key, value in self._cfg.items():
            cfg_path = self.CFG_POOL.query(key, value)
            if cfg_path is not None:
                # cfg_path should be a list
                for cfg_path_ in cfg_path:
                    sub_cfg = CFGLoader().load_cfg(cfg_path_)
                    if _cfg is None:
                        _cfg = sub_cfg
                    else:
                        _cfg.update(sub_cfg)
        if _cfg is not None:
            _cfg.update(self._cfg)
            self._cfg = _cfg

    @staticmethod
    def snake_to_camel(snake):
        splited_snake = snake.split('_')
        splited_camel = [word.capitalize() for word in splited_snake]
        camel = ''.join(splited_camel)
        return camel

    def post_config(self):
        self._cfg['group'] = self.GROUP_NAME
        if 'id' not in self._cfg:
            d = datetime.datetime.now()
            date_str = d.strftime('%Y%m%d_%H%M%S')
            group_name = self.snake_to_camel(self.GROUP_NAME)
            self._cfg['id'] = f'{group_name}_{date_str}'

    def get(self, key, default=None, warn=False):
        undefined = self._cfg.get(key, None) is None
        if undefined and warn:
            print(f'[Opts Warn] {key} undefined, '
                   f'use default value ({default}).')
        return self._cfg.get(key, default)

    def set(self, key, value):
        self._cfg[key] = value
        setattr(self, key, value)

    def update(self, data: dict, override: bool=False) -> None:
        for key, value in data.items():
            if hasattr(self, key) and not override:
                continue
            self.set(key, value)

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

    def __contains__(self, key):
        return key in self._cfg.keys()

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

    def dump_pkl(self, file_path):
        # dump as yaml file
        file_path = f'{file_path}.pkl'
        with open(file_path, 'wb') as f:
            pickle.dump(self._cfg, f)

    def load_pkl(self, file_path, update=True):
        file_path = f'{file_path}.pkl'
        with open(file_path, 'rb') as f:
            cfg = pickle.load(f)
        self.loads(cfg, update)

    def loads(self, cfg, update=False):
        if update:
            cfg.update(self._cfg)
            self._cfg = cfg
        else:
            self._cfg = cfg
        self.set_attr()

    def perfect(self):
        cfg = self.dumps()
        string = ''
        for key, val in cfg.items():
            string += f'{key}: {val}\n'

        return string

    def __str__(self) -> str:
        return self.perfect()

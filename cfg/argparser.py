import argparse
from collections import defaultdict


class CFGPool(object):
    def __init__(self):
        self._dict = defaultdict(lambda: None)
    
    def regist(self, key, value, cfg_path):
        if self._dict[key] is None:
            self._dict[key] = {value: cfg_path}
        else:
            self._dict[key][value] = cfg_path

    def query(self, key, value) -> str:
        if not key in self._dict.keys():
            return None
        else:
            try:
                return self._dict[key][value]
            except KeyError:
                raise RuntimeError(
                    f'Excepct {value} in {key} cfg pool.')


class Args(object):
    ARG_CFGS = []
    CFG_POOL = CFGPool()

    def __init__(self, description=None):
        self._parser = argparse.ArgumentParser(description)
        self._args = None
        self._dict = {}

    def parse(self, args=None):
        for item in self.ARG_CFGS:
            name = item.pop('name')
            self._parser.add_argument(name, **item)
        self._args = self._parser.parse_args(args)
        self._dict = self._args.__dict__
        return self

    @property
    def dict(self):
        return self._dict

    def __getitem__(self, name):
        return self._dict[name]

    @classmethod
    def reset(cls):
        cls.ARG_CFGS = []

    @staticmethod
    def ext_name(name):
        if '--' in name:
            return name
        if '-' in name:
            raise NameError(f'Invalid name [{name}].')
        return f'--{name}'

    @classmethod
    def add_with_dict(cls, data):
        for k, v in data.items():
            help = f'arg for {k}'
            if isinstance(v, int):
                cls.add_int(k, help=help, default=v)
            elif isinstance(v, float):
                cls.add_float(k, help=help, default=v)
            elif isinstance(v, bool):
                cls.add_bool(k, help=help, default=v)
            elif isinstance(v, str):
                cls.add_string(k, help=help, default=v)
            elif isinstance(v, list):
                cls.add_list(k, v[0].__class__, default=v, help=help)

    @classmethod
    def add_yml(cls, key, value, cfg_path):
        cls.CFG_POOL.regist(key, value, cfg_path)

    add_yaml = add_yml

    @classmethod
    def add_bool(cls, name, default=None, help=None, required=False):
        help = help or f'{name}: bool'
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': bool,
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_int(cls, name, default=None, help=None, required=False):
        help = help or f'{name}: int'
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': int,
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_float(cls, name, default=None, help=None , required=False):
        help = help or f'{name}: float'
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': float,
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_string(cls, name, default=None, help=None, required=False):
        help = help or f'{name}: str'
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': str,
                'required': required}
        cls.ARG_CFGS.append(item)
    
    @classmethod
    def add_list_int(cls, name, default=None, help=None, required=False):
        help = help or f'{name}: [*int]'
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': int,
                'nargs': '+',
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_list_float(cls, name, default=None, help=None, required=False):
        help = help or f'{name}: [*float]'
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': float,
                'nargs': '+',
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_list_string(cls, name, default=None, help=None, required=False):
        help = help or f'{name}: [*str]'
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': str,
                'nargs': '+',
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_list(cls, name, type, default=None, help=None, required=False):
        help = help or f'{name}: {type}'
        if type is int:
            cls.arg_list_int(name=name, help=help,
                             default=default, required=required)
        elif type is float:
            cls.arg_list_float(name=name, help=help,
                               default=default, required=required)
        elif type is str:
            cls.arg_list_string(name=name, help=help,
                                default=default, required=required)
        else:
            raise ValueError(f'Not support list type [{type}]')

import argparse


class Args(object):
    ARG_CFGS = []

    def __init__(self, description=None):
        self.description = description
        self.parser = argparse.ArgumentParser(description=self.description)
        self.args = None
        self.dict = {}

    def parse(self, args=None):
        for item in self.ARG_CFGS:
            name = item.pop('name')
            self.parser.add_argument(name, **item)
            self.args = self.parser.parse_args(args)
            self.dict = self.args.__dict__
        return self

    def __getitem__(self, name):
        return self.dict[name]

    @classmethod
    def reset(cls):
        cls.ARG_CFGS = []

    @staticmethod
    def ext_name(name):
        if '--' in name:
            return name
        if '-' in name:
            raise NameError(f'Invalid name {name}.')
        return f'--{name}'

    @classmethod
    def add_bool(cls, name, help, default=None, required=False):
        if default is True:
            action = 'store_true'
        elif default is False:
            action = 'store_false'
        else:
            raise ValueError('True or False are required.')

        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'action': action,
                'type': bool,
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_int(cls, name, help, default=None, required=False):
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': int,
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_float(cls, name, help, default=None, required=False):
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': float,
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_string(cls, name, help, default=None, required=False):
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': str,
                'required': required}
        cls.ARG_CFGS.append(item)
    
    @classmethod
    def add_list_int(cls, name, help, default=None, required=False):
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': int,
                'nargs': '+',
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_list_float(cls, name, help, default=None, required=False):
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': float,
                'nargs': '+',
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_list_string(cls, name, help, default=None, required=False):
        item = {'name': cls.ext_name(name),
                'help': help,
                'default': default,
                'type': str,
                'nargs': '+',
                'required': required}
        cls.ARG_CFGS.append(item)

    @classmethod
    def add_list(cls, name, help, type, default=None, required=False):
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

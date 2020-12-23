import os
from yaml import dump
from cfg import Opts


def test_default_args():
    Opts.reset()
    Opts.add_int('a', 'a value', 1)

    opt = Opts()
    assert opt.a == 1

    opt.b = 2

    assert opt['b'] == 2

    data = opt.dumps()
    assert data['b'] == 2


    data1 = opt.dumps()
    opt.loads(data, update=False)
    data2 = opt.dumps()

    for k in data1.keys():
        assert data1[k] == data2[k]

    # =================
    dumped_yaml_file = 'dumped_yaml_file.yaml'

    opt.dump(dumped_yaml_file)
    opt._cfg = {}
    assert not opt._cfg
    opt.load(dumped_yaml_file)

    for k in data1.keys():
        assert data1[k] == opt[k]

# ======================================

yaml_file = 'yaml_test.yaml'


def create_yaml_file(data, file=None):
    with open(file or yaml_file, 'w') as f:
        for k, v in data.items():
            if not isinstance(v, list):
                f.write(f'{k}: {v}\n')
            else:
                f.write(f'{k}:\n')
                for item in v:
                    f.write(f'  - {item}\n')
    

def remove_yaml_file():
    if os.path.exists(yaml_file):
        os.remove(yaml_file)


def test_opts_load_yaml():
    Opts.reset()
    try:
        data = {'name': 'linux'}
        create_yaml_file(data)
        opt = Opts(yaml_file)
        assert opt['name'] == data['name']
    except Exception as e:
        raise e
    #======================
    finally:
        remove_yaml_file()


def test_yaml_to_arg():
    Opts.reset()
    try:
        data = {'name': 'linux'}
        create_yaml_file(data)
        opt = Opts(yaml_file, _parse_data='--name unix'.split(' '))

        assert opt['name'] == 'unix'
    except Exception as e:
        raise e
    #======================
    finally:
        remove_yaml_file()
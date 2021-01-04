import os
from yaml import dump
from cfg import Opts


def test_default_args():
    Opts.reset()
    Opts.add_int('a', 1, 'a value')

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
    try:
        dumped_yaml_file = 'dumped_yaml_file.yaml'

        opt.dump(dumped_yaml_file)
        opt._cfg = {}
        assert not opt._cfg
        opt.load(dumped_yaml_file)

        for k in data1.keys():
            assert data1[k] == opt[k]
    except Exception as e:
        raise e
    finally:
        remove_yaml_file(dumped_yaml_file)

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
    

def remove_yaml_file(file=None):
    if os.path.exists(file or yaml_file):
        os.remove(file or yaml_file)


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


def test_arg_list():
    Opts.reset()

    lst = [1, 2, 3]
    Opts.add_list_int('a', lst, 'a list')
    opt = Opts()
    for item in lst:
        assert item in opt.a
    for item in opt.a:
        assert item in lst

    # ============================
    Opts.reset()
    lst = [1, 2, 3]
    lst2 = [4, 5, 6]
    Opts.add_list_int('a', lst, 'a list')
    parse_data = f"--a {' '.join(str(i) for i in lst2)}".split(' ')
    opt = Opts(_parse_data=parse_data)
    for item in lst2:
        assert item in opt.a
    for item in opt.a:
        assert item in lst2

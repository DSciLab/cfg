import os

import yaml
from cfg.yaml_loader import YAMLLoader


yaml_file = 'yaml_test.yaml'
sub_yaml_file = 'sub_yaml_test.yaml'

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

    if os.path.exists(sub_yaml_file):
        os.remove(sub_yaml_file)


def test_load():
    try:
        data = {'name': 'linux'}
        create_yaml_file(data)
        yaml_loader = YAMLLoader(yaml_file)
        assert yaml_loader['name'] == data['name']

        # ======================
        data = {'list': [1, 2, 3]}
        create_yaml_file(data)
        yaml_loader = YAMLLoader(yaml_file)
        assert yaml_loader['list'] == data['list']
    except Exception as e:
        raise e
    #======================
    finally:
        remove_yaml_file()


def test_auto_file_ext():
    root_path = 'a/b/c/mm.yaml'
    file_path = 'z.yaml'

    final_path = YAMLLoader.auto_file_ext(root_path, file_path)
    assert final_path == 'z.yaml'

    # =======================
    root_path = 'a/b/c/mm.yaml'
    file_path = 'z.yml'

    final_path = YAMLLoader.auto_file_ext(root_path, file_path)
    assert final_path == 'z.yml'

    # =======================
    root_path = 'a/b/c/mm.yaml'
    file_path = 'z'

    final_path = YAMLLoader.auto_file_ext(root_path, file_path)
    assert final_path == 'z.yaml'

    # =======================
    root_path = 'a/b/c/mm.yml'
    file_path = 'z'

    final_path = YAMLLoader.auto_file_ext(root_path, file_path)
    assert final_path == 'z.yml'


def test_get_relative_path():
    root_path = 'a/b/c/mm.yaml'
    file_path = 'z.yaml'

    final_path = YAMLLoader.get_relative_path(root_path, file_path)
    assert final_path == 'a/b/c/z.yaml'

    # ======================
    root_path = 'a/b/c/mm.yaml'
    file_path = './z.yaml'

    final_path = YAMLLoader.get_relative_path(root_path, file_path)
    assert final_path == 'a/b/c/z.yaml'

    # ======================
    root_path = 'a/b/c/mm.yaml'
    file_path = '../z.yaml'

    final_path = YAMLLoader.get_relative_path(root_path, file_path)
    assert final_path == 'a/b/z.yaml'

    # ======================
    root_path = 'a/b/c/mm.yaml'
    file_path = '../../z.yaml'

    final_path = YAMLLoader.get_relative_path(root_path, file_path)
    assert final_path == 'a/z.yaml'

    # ======================
    root_path = 'a/b/c/mm.yaml'
    file_path = '../x/z.yaml'

    final_path = YAMLLoader.get_relative_path(root_path, file_path)
    assert final_path == 'a/b/x/z.yaml'


def test_import_cfg():
    try:
        main_data = {'import': sub_yaml_file, 'a': 1}
        sub_data = {'b': 2}
        create_yaml_file(main_data, yaml_file)
        create_yaml_file(sub_data, sub_yaml_file)

        yaml_loader = YAMLLoader(yaml_file)
        assert yaml_loader['a'] == main_data['a']
        assert yaml_loader['b'] == sub_data['b']

        # ==============================
        main_data = {'import': sub_yaml_file, 'a': 1}
        sub_data = {'a': 2}
        create_yaml_file(main_data, yaml_file)
        create_yaml_file(sub_data, sub_yaml_file)

        yaml_loader = YAMLLoader(yaml_file)
        assert yaml_loader['a'] == sub_data['a']

    # =====================
    except Exception as e:
        raise e
    finally:
        remove_yaml_file()
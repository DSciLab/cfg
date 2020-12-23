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

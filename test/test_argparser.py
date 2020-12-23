from cfg.argparser import Args


def test_arg_int():
    name = 'arg_name'
    help = 'arg_help'
    default = 100

    Args.add_int(name, help, default)
    arg = Args().parse()
    assert arg[name] == default

    name = 'arg_name'
    help = 'arg_help'
    default = 100

    Args.reset()
    Args.add_int(name, help, default)
    print(Args.ARG_CFGS)
    arg = Args().parse('--arg_name 200'.split(' '))
    assert arg[name] == 200

    Args.reset()
    Args.add_int(name, help, default)
    print(Args.ARG_CFGS)
    try:
        arg = Args().parse('--arg_name 20.3'.split(' '))
    except:
        pass
    else:
        assert False

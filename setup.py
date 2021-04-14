from distutils.core import setup
import datetime


def gen_code():
    d = datetime.datetime.now()
    date_str = d.strftime('%Y%m%d%H%M%S')
    return f'dev{date_str}'


__version__ = f'0.0.1-{gen_code()}'


setup(name='cfg_dist',
      version=__version__,
      description='Auto configuration',
      author='tor4z',
      author_email='vwenjie@hotmail.com',
      install_requires=[
            'PyYAML'
      ],
      packages=['cfg'],
     )

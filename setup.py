from distutils.core import setup
import cfg


setup(name='cfg_dist',
      version=cfg.__version__,
      description='Auto configuration',
      author='tor4z',
      author_email='vwenjie@hotmail.com',
      install_requires=[
            'PyYAML'
      ],
      packages=['cfg'],
     )

from setuptools import find_packages, setup

setup(name='pin',
      version='0.0.1',
      install_requires=['torch>=1.1.0', 'torchvision>=0.3', 'numpy', 'gensim',
                        'tqdm', 'pandas', 'Munch'],
      packages=find_packages())

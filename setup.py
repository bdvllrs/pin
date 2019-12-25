from setuptools import find_packages, setup

setup(name='pin',
      version='0.0.6',
      py_modules=['pin'],
      install_requires=['sacred', 'Click', 'omegaconf==1.4.1', 'ruamel.yaml'],
      packages=find_packages(),
      package_data={'pin': ['templates/config/*',
                            'templates/*',
                            'templates/scripts/*']},
      include_package_data=True,
      entry_points="""
      [console_scripts]
      pin=pin.cli.main:cli
      """)

from setuptools import find_packages, setup

setup(name='pin',
      version='0.0.4',
      py_modules=['pin'],
      install_requires=['sacred', 'Click'],
      packages=find_packages(),
      include_package_data=True,
      entry_points="""
      [console_scripts]
      pin=pin.cli.main:cli
      """)

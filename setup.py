from setuptools import find_packages, setup

setup(name='pin',
      version='0.0.3',
      py_modules=['pin'],
      install_requires=['sacred', 'Click'],
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      pin=pin.pin:cli
      """)

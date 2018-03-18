from setuptools import setup

setup(
    name='cliapp',
    version='0.1.0',
    packages=['cliapp'],
    entry_points={'console_scripts': ['cliapp = cliapp.__main__:main']})

import os
from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Get install requires
requirements = f'{os.path.dirname(os.path.realpath(__file__))}/requirements.txt'

if os.path.isfile(requirements):
    with open(requirements) as f:
        install_requires = f.read().splitlines()

setup(
    name='todoist-extractor',
    version='0.0.0',
    description='A practical Todoist log activity extractor',
    author='Clovis',
    author_email='clovisguerim@gmail.com',
    url='https://github.com/clovisguerim',
    packages=find_packages(exclude='docs'),
    entry_points='''
        [console_scripts]
        todoist-extractor=cli:main
    ''',
    install_requires=install_requires,
    data_files=[('requirements', ['requirements.txt'])]
)

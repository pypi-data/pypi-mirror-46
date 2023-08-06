from setuptools import setup

from os import path
from dipr.Utilities.Version import DIPR_VERSION

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dipr',
    version=DIPR_VERSION,
    packages=['Repos', 'Errors', 'Commands', 'Settings', 'Arguments', 'Protocols', 'Protocols.Hg', 'Protocols.Hg.hglib',
              'Protocols.Git', 'Utilities', 'Templates'],
    package_dir={
        '': 'dipr',
        'Templates': 'dipr/Templates'
    },
    package_data={
        'Templates': ['dipr/Templates/*.yaml']
    },
    url='http://www.dipr.dev',
    license='MIT',
    author='ZaXa Software, LLC',
    author_email='info@zaxasoft.com',
    description='A revision control independent dependency and sub-repository management package.',

    include_package_data=True,
    install_requires=[
        'ruamel.yaml',
        'GitPython'
    ],
    long_description = long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
              'dipr = Commands.command_line:main'
        ]
    }
)
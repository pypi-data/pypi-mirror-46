
#
# @filename    : setup.py
# @description : The traditional setup.py script for
#                Installation from pip or easy_install

from codecs import open
from os.path import abspath, dirname, join
from setuptools import setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='socialist',
    version='0.1.0',
    long_description=long_description,
    url='https://github.com/OverwatchHeir/SociaList',
    download_url='https://github.com/OverwatchHeir/SociaList/archive/master.zip',
    author='OverwatchHeir',
    author_email='softw.dev@protonmail.com',
    license="GNU",
    install_requires=[
        'tqdm',
        'phonenumbers',
        'validate_email',
        'py3dns'
    ],
    classifiers=[
        'Topic :: Utilities',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7'
    ],
    packages=['socialist'],
    entry_points={
        'console_scripts': ['socialist = socialist.socialist:main']
    }


)
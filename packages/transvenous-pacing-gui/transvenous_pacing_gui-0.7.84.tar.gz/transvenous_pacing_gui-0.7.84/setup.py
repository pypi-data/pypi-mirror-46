# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import transvenous_pacing_gui

with open('README.md') as f:
    readme = f.read()

requirements = [
    'matplotlib',
    'pyserial',
    'numpy'
]

setup(
    name='transvenous_pacing_gui',
    version='0.7.84',
    description='Transvenous pacing procedure simulation GUI written in Python 3',
    long_description=readme,
    author='Nam Tran, Cooper Pearson, Richie Beck, Marcel Isper, Brianna Cathey',
    author_email='tranngocnam97@gmail.com',
    url='https://github.com/omn0mn0m/transvenous_pacing_gui',
    license="MIT license",
    packages=find_packages(exclude=('tests', 'docs')),
    tests_require=['pytest'],
    extras_require={
        'testing': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'transvenous_pacing_gui = transvenous_pacing_gui.gui:main',
        ],
    },
    install_requires=requirements,
)

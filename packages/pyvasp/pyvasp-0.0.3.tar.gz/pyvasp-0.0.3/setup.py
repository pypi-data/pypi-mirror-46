#!/usr/bin/env python3

from setuptools import setup

setup(
    name='pyvasp',
    version='0.0.3',
    author='Wenbo Fu',
    author_email='ltaiwb@outlook.com',
    description='Multi-option command line tool for VASP',
    long_description=open('README.md').read(),
    url='https://github.com/ltaiwb/pyvasp',
    license='MIT',
    packages=['pyvasp'],
    install_requires=['numpy', 'matplotlib', 'scipy'],
    entry_points = {'console_scripts':['pv = pyvasp.pyvasp:main']},
    classifiers = [
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Chemistry']
)

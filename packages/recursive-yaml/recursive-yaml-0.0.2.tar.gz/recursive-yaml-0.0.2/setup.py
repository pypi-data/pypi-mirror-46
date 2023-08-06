"""
recursive-yaml
Load YAML Recursively
Author: SF-Zhou
Date: 2019-04-09
"""

from setuptools import setup

name = 'recursive-yaml'
module = name.replace("-", "_")
setup(
    name=name,
    version='0.0.2',
    description='Load YAML Recursively',
    url=f'https://github.com/FebruaryBreeze/{name}',
    author='SF-Zhou',
    author_email='sfzhou.scut@gmail.com',
    keywords='Recursive YAML',
    entry_points={
        'console_scripts': [f'{name}={module}:main'],
    },
    py_modules=[f'{module}'],
    install_requires=['PyYAML']
)

"""
torch-model-state
PyTorch Model State Save & Load
Author: SF-Zhou
Date: 2019-04-10
"""

from setuptools import find_packages, setup

name = 'torch-model-state'
module = name.replace("-", "_")
setup(
    name=name,
    version='0.0.6',
    description='PyTorch Model State Save & Load',
    url=f'https://github.com/FebruaryBreeze/{name}',
    author='SF-Zhou',
    author_email='sfzhou.scut@gmail.com',
    keywords='PyTorch Model State',
    packages=find_packages(exclude=['tests', f'{module}.configs.build']),
    package_data={f'{module}': ['schema/*.json']},
    entry_points={
        'console_scripts': [f'{name}={module}:cli_main'],
    },
    install_requires=[
        'argparse-schema',
        'box-box',
        'jsonschema',
        'json-schema-to-class>=0.1.3',
        'torch',
    ]
)

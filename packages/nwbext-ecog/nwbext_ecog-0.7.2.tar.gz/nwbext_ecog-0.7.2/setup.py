from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nwbext_ecog',
    version='0.7.2',
    description='Convert data to nwb',
    long_description=long_description,
    author='Ben Dichter',
    author_email='ben.dichter@gmail.com',
    keywords=['nwb', 'extension'],
    install_requires=['pynwb'],
    packages=find_packages(),
    data_files=[('ndx_specs', ['spec/ecog.namespace.yaml', 'spec/ecog.extensions.yaml'])]
)

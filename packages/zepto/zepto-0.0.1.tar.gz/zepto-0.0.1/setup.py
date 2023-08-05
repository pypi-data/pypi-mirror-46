from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zepto',
    version='0.0.1',
    author='Niranjan Rajendran',
    author_email='pypi@niranjan.io',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='gpl-3.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        zepto=zepto.scripts.cli:cli
    ''',
)

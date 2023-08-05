# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='pltshow',
    version='0.1.1',
    description='client for pltshow',
    long_description='client for pltshow to update dataset',
    author='quicksort',
    author_email='quicksort@outlook.com',
    url='https://github.com/quick-sort/pltshow-sdk',
    include_package_data=True,
    install_requires=['requests', 'pandas'],
    py_modules=['pltshow'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    packages=find_packages(exclude=('tests', 'docs'))
)

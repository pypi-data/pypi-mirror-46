#!/usr/bin/env python
from setuptools import find_packages, setup

project = "almetro"
version = "1.0.0"

setup(
    name=project,
    version=version,
    license="Apache License",
    description="A python library to measure algorithms execution time and compare with its theoretical complexity",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Arnour Sabino",
    author_email="arnour.sabino@gmail.com",
    url="https://github.com/arnour/almetro",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "matplotlib==3.0.3",
        "tabulate==0.8.3"
    ],
    setup_requires=[
        "nose>=1.3.7",
    ],
    dependency_links=[
    ],
    entry_points={
    },
    extras_require={
        "test": [
            "flake8>=3.7.7",
            "flake8-print>=3.1.0",
            "coverage>=4.5.3",
            "PyHamcrest>=1.9.0",
        ],
    },
)

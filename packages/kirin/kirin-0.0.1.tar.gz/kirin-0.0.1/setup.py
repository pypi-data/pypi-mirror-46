from setuptools import setup, find_packages
from kirin import __version__

import os
from setuptools import setup, find_packages


setup(
    name="kirin",
    version=__version__,
    url="https://github.com/ericmjl/kirin",
    author="Eric J. Ma",
    author_email="ericmajinglong@gmail.com",
    description="Deploy to PyPI on PR merge.",
    packages=["kirin"],
    install_requires=["twine", "bumpversion"],
    entry_points={"console_scripts": ["kirin=kirin.cli:main"]},
)

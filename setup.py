#!/usr/bin/env python

import os
from setuptools import setup, find_packages

# allow setup.py to be ran from anywhere
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def parse_requirements():
    with open("requirements.txt", "rt") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith(("#", "-")):
                continue
            yield line


setup(
    name="multidocs",
    version="0.1.2",
    license="GPL-3.0",
    description="Generate documentation from multiple sources.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andreas Lutro",
    author_email="anlutro@gmail.com",
    url="https://github.com/anlutro/multidocs",
    install_requires=list(parse_requirements()),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)

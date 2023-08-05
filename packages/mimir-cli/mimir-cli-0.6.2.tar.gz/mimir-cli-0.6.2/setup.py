#!/usr/bin/env python
"""
pip setup file for mimir-cli
"""
from setuptools import setup, find_packages
from mimir_cli.globals import __version__, PACKAGE


with open("README.rst") as readme:
    long_description = readme.read()

setup(
    name=PACKAGE,
    version=__version__,
    description="mimir cli application",
    long_description=long_description,
    author="Jacobi Petrucciani",
    author_email="jacobi@mimirhq.com",
    url="",
    py_modules=[PACKAGE],
    download_url="",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Environment :: Console",
    ],
    platforms=["Any"],
    scripts=[],
    provides=[],
    install_requires=["click>=7.0", "requests"],
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["mimir = mimir_cli.mimir:cli"]},
)

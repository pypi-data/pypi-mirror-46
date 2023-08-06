#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="pulp-cookbook",
    version="0.0.4b3",
    description="Cookbook plugin for the Pulp Project",
    long_description=long_description,
    author="Simon Baatz",
    author_email="gmbnomis@gmail.com",
    url="https://github.com/gmbnomis/pulp_cookbook/",
    install_requires=["pulpcore-plugin~=0.1rc2"],
    extras_require={"postgres": ["pulpcore[postgres]"], "mysql": ["pulpcore[mysql]"]},
    include_package_data=True,
    packages=find_packages(exclude=["test"]),
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ),
    entry_points={"pulpcore.plugin": ["pulp_cookbook = pulp_cookbook:default_app_config"]},
)

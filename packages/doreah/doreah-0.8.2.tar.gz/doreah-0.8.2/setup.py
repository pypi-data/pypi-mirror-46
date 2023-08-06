import setuptools
import importlib

module = importlib.import_module(setuptools.find_packages()[0])

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doreah",
    version=".".join(str(n) for n in module.version),
    author="Johannes Krattenmacher",
    author_email="python@krateng.dev",
    description="Small toolkit of utilities for python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krateng/doreah",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)

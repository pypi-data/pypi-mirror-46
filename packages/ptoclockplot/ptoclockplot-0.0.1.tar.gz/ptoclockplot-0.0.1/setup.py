# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ptoclockplot",
    version="0.0.1",
    author="Eric Cramer",
    author_email="eric.cramer@curie.fr",
    description="A package for plotting clusters in a simple \"pseudo-temporal-ordering\", like a clock face.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emcramer/clockplot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
import pathlib

from setuptools import setup
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE/ "README.md").read_text()

setup(
    name="CFBScrapy",
    version="0.1.02",
    description="Python wrapper for the collegefootballapi located here: https://api.collegefootballdata.com/api/docs/?url=/api-docs.json#/",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rlindholm/CFBScrapy",
    author="Ryan Lindholm",
    author_email="ryan.lindholm@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=["requests", "pandas", "json", "pandas.io"],
    
)
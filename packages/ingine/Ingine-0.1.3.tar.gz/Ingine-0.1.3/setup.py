from setuptools import setup, find_packages

import Ingine

with open("README.md", "r") as fh:
    long_description = fh.read()

print(find_packages())

setup(
    name = "Ingine",
    version = Ingine.__version__,
    author = "sqarrt",
    author_email = "sqarrt1337@gmail.com",
    description = "A cross-platform library for easy-access AI tools",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/sqarrt/ingine",
    packages = find_packages(),
    install_requires = ['keras',
                        'numpy',
                        'tensorflow',
                        'theano',
                        'pyeasyga'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Russian",
    ],
)

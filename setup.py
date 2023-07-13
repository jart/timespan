import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name                 = "timespan",
    version              = '0.2.0',
    description          = "Utilities for Asterisk and Microsoft .Net timespans",
    long_description     = read("README.md"),
    long_description_content_type = 'text/markdown',
    author               = "Justine Tunney",
    author_email         = "jtunney@gmail.com",
    url                  = "https://github.com/jart/timespan",
    license              = "MIT",
    python_requires      = ">=2.7",
    install_requires     = [],
    packages             = find_packages(include=['timespan', 'timespan.*']),
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
    ],
)

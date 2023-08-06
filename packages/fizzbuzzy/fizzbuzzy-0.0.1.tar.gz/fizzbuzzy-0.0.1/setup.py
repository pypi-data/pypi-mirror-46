"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/santhoshse7en/FizzBuzz
"""
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

# Always prefer setuptools over distutils
import setuptools

setuptools.setup(
    name="fizzbuzzy",
    version="0.0.1",
    author="M Santhosh Kumar",
    author_email="santhoshse7en@gmail.com",
    description="Python package which prints Fizz, Buzz, FizzBuzz divisible by 3 and 5 and both",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/santhoshse7en/FizzBuzz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# Causes `python setup.py test` to not crash.
# See https://groups.google.com/forum/#!msg/nose-users/fnJ-kAUbYHQ/_UsLN786ygcJ
import multiprocessing  # noqa
from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(name='urbandict',
      version='0.6.1',
      py_modules=['urbandict'],
      scripts=['urbandicli'],
      author='Roman Bogorodskiy',
      author_email='bogorodskiy@gmail.com',
      description='CLI client and a library for urbandictionary.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/novel/py-urbandict',
      classifiers=[
                "Environment :: Console",
                "Intended Audience :: End Users/Desktop",
                "Intended Audience :: Developers",
                "License :: Public Domain",
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 3",
            ],)

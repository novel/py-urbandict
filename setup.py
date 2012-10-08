# Causes `python setup.py test` to not crash.
# See https://groups.google.com/forum/#!msg/nose-users/fnJ-kAUbYHQ/_UsLN786ygcJ
import multiprocessing
from setuptools import setup

setup(name='urbandict',
        version='0.2',
        py_modules=['urbandict'],
        scripts=['urbandicli'],
        test_suite='nose.collector',
        test_requires=['nose', 'mock'],
        classifiers=[
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 3",
            ],
        )

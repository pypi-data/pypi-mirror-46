#!/usr/bin/env python

from setuptools import setup

long_desc = \
"""
Here it is, another Python terminal logger: apytl. This implementation
 relies only on the Python standard library, and uses the `logging` module
 to emit messages. This ensure that messages are output to the terminal
 even if whatever is calling apytl is doing so from within a shell script.
"""

setup(
    name='apytl',
    version='0.0a1',
    author='Andrew Nadolski',
    author_email='andrew.nadolski@gmail.com',
    description='A bawdy, emoji-friendly progress bar.',
    longi_description=long_desc,
    platforms=['Linux', 'MacOS X'],
    url='https://github.com/anadolski/apytl',
    python_requires='>=3.6',
    package_dir={'apytl': 'apytl'},
    packages=['apytl'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 3 - Alpha',
        ],
    )

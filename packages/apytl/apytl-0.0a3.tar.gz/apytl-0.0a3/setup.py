#!/usr/bin/env python

from setuptools import setup

with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='apytl',
    version='0.0a3',
    author='Andrew Nadolski',
    author_email='andrew.nadolski@gmail.com',
    description='A bawdy, emoji-friendly progress bar.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
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

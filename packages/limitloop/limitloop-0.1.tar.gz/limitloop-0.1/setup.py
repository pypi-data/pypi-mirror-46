#!/usr/bin/env python3
from setuptools import setup

SHORT_DESC = 'Limitloop is a lightweight python module for running loops that depend on precise timing.'

with open('README.md', 'r') as readme_file:
    readme_contents = readme_file.read()

setup(
    name='limitloop',
    version=0.1,
    author='Alex Medeiros',
    author_email='alex.daniel.medeiros@gmail.com',
    url='https://github.com/Alex-Medeiros/limitloop',
    description=SHORT_DESC,
    long_description=readme_contents,
    long_description_content_type='text/markdown',
    packages=['limitloop'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python'
    ],
    license='GPLv3'
)

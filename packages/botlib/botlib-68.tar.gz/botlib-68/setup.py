#!/usr/bin/env python3

""" setup.py """

from setuptools import setup

setup(
    name='botlib',
    version='68',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots",
    long_description=""" BOTLIB is a pure python3 framework to program bots (a botlib), provides a IRC bot and is extendible by programming your own commands. 
                         BOTLIB has been placed in the Public Domain and contains no copyright or LICENSE.
                     """,   
    license='Public Domain',
    install_requires=["obj"],
    packages=["bot"],
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python'
                ]
)

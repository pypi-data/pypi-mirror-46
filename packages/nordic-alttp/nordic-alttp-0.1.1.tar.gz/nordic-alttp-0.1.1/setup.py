# -*- coding: utf-8 -*-

# python std lib
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ""
history = ""

setup(
    name="nordic-alttp",
    version="0.1.1",
    description="",
    long_description=readme + '\n\n' + history,
    author="Johan Andersson",
    author_email="Grokzen@gmail.com",
    maintainer='Johan Andersson',
    maintainer_email='Grokzen@gmail.com',
    packages=["alttp"],
    url='',
    license='MIT',
    install_requires=[
        'aioconsole',
        'asyncio',
        'websockets',
        'colorama'
    ],
    keywords=[],
    entry_points={
        'console_scripts': [
            'multiworld = alttp.MultiClient:cli_entrypoint',
        ],
    },
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Web Environment',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
    ]
)

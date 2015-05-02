"""
===============
Wodify2

A tool for downloading Wodify
weight-lifting metrics. That allows you to compare
athlete's against each other.
===============
"""
from os import environ
from distutils.core import setup

__version__ = "0.1.0"


def install_requires():
    """Check for required packages"""
    skip_install_requires = environ.get('SKIP_INSTALL_REQUIRES')
    if not skip_install_requires:
        with open('requirements.pip') as r:
            return r.readlines()
    return []


setup(
    author = "Eloy Zuniga Jr.",
    author_email = "eloyz.email@gmail.com",
    description = "wodify_downloader",
    long_description = __doc__,
    fullname = "wodify_downloader",
    name = "wodify_downloader",
    # url = "https://github.com/eloyz/wodify_downloader",
    # download_url = "https://github.com/eloyz/wodify_downloader",
    version = __version__,
    platforms = ["Linux"],
    packages = [
        "wodify2",
        "wodify2.bin",
    ],
    install_requires = install_requires(),
    entry_points = {
        'console_scripts': [
            "wodify-download = wodify2.bin.download:main",
            "wodify-merge = wodify2.bin.merge:main",
            "wodify-save = wodify2.bin.save:main",
            "wodify-transform = wodify2.bin.transform:main",
            "wodify-dbcreate = wodify2.bin.db_create:main"
        ]
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Server Environment",
        "Intended Audience :: Developers",
        "Operating System :: Linux",
        "Programming Language :: Python",
    ]
)

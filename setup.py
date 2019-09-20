# -*- coding: utf-8 -*-
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='natas',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.3',

    description='Python library for processing historical English',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://github.com/mikahama/natas',

    # Author details
    author='Mika Hämäläinen, Dept. of  Digital Humanities, University of Helsinki',
    author_email='mika.hamalainen@helsinki.fi',

    # Choose your license
    license='Apache License, Version 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        "Topic :: Text Processing :: Linguistic",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',

    ],

    # What does your project relate to?
    keywords='historical English, spelling normalization, OCR error correction',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=["natas"],
    package_dir={'natas': 'natas'},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["configargparse","distance", "torch==1.0.0", "torchtext>=0.4.0@https://mikakalevi.com/downloads/text-master.zip#egg=torchtext-0.4.0", "spacy>=2.1.4", "mikatools>=0.0.6",r"OpenNMT-py>=0.8.2@https://github.com/OpenNMT/OpenNMT-py/archive/0.8.2.zip#egg=OpenNMT-py-0.8.2", r"en_core_web_md>=2.1.0@https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.1.0/en_core_web_md-2.1.0.tar.gz#egg=en_core_web_md-2.1.0"],
    dependency_links=["https://mikakalevi.com/downloads/text-master.zip#egg=torchtext-0.4.0","https://github.com/OpenNMT/OpenNMT-py/archive/0.8.2.zip#egg=OpenNMT-py-0.8.2", "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.1.0/en_core_web_md-2.1.0.tar.gz#egg=en_core_web_md-2.1.0"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'natas': ['models/*.txt', "wiktionary_lemmas.json"],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={},
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/mikahama/natas/issues',
        'Developer': 'https://mikakalevi.com/'
    },
)
Kauri ID Python Library
=======================

A (reference) library of tools to support work with the Kauri ID data
structures and protocols.


Installation/Usage
------------------

To install use pip:

    $ pip install pykauriid


Or clone the repo:

    $ git clone https://gitlab.com/kauriid/pykauriid.git
    $ python setup.py install

Set up and activate for Python 3:

    virtualenv ${HOME}/.virtualenvs/pykauriid \
               --system-site-packages --python=/usr/bin/python3
    source ${HOME}/.virtualenvs/pykauriid/bin/activate

Install required packages:

    pip install -e .

For installing the additional development, testing or documentation
dependencies, add a qualifier with one or more of these commands:

    pip install -e .[dev]           # Development dependencies
    pip install -e .[test]          # Testing dependencies
    pip install -e .[doc]           # Documentation dependencies
    pip install -e .[dev,test,doc]  # All dependencies together


Contributing
------------

TBD


Example
-------

TBD


## Licence

Copyright 2018-2019 by SingleSource Limited, Auckland, New Zealand

This work is licensed under the Apache 2.0 open source licence.
Terms and conditions apply.

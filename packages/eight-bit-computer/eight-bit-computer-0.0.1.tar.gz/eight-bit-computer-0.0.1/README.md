# 8 bit Computer

[![Documentation Status](https://readthedocs.org/projects/eight-bit-computer/badge/?version=master)](https://eight-bit-computer.readthedocs.io/en/master/?badge=master)

[![Coverage Status](https://coveralls.io/repos/github/ninezerozeronine/eight-bit-computer/badge.svg?branch=master)](https://coveralls.io/github/ninezerozeronine/eight-bit-computer?branch=master)

This is a project to make a basic but fully functional 8 bit computer 
using 7400 series ICs.

The full docs can be found on the Read the Docs: https://eight-bit-computer.readthedocs.io/

# Docs

To build the docs on mac run:

    make clean
    make html

in `docs`.

To build the docs in windows run:

    sphinx-build.exe . _build

in `docs`.

# Tests

To run the tests, run:

    tox -e test

in the root directory.

To generate a coverage report run:

    tox -e cov

in the root directory.

# License

The content of this project itself is licensed under the
[Attribution-ShareAlike 4.0 International
license](http://creativecommons.org/licenses/by-sa/4.0/), and any source code used
in conjunction with the project is licensed under the [MIT
license](http://opensource.org/licenses/mit-license.php).
[![Build Status](https://travis-ci.org/korpling/graphANNIS-python.svg?branch=develop)](https://travis-ci.org/korpling/graphANNIS-python)

graphANNIS Python Bindings
==========

GraphANNIS is a library for corpus linguistic queries.
This are the Python bindings to its API.

How to use in your own scripts
------------------------------

GraphANNIS is available as Python3-compatible library from the central PyPI repository: https://pypi.org/project/graphannis/
You can install it locally with *pip* (https://pip.pypa.io/en/stable/).
```
pip install graphannis
```
On Ubuntu Linux systems the command might be `pip3`for Python 3.

You can view the [API documentation online](http://graphannis-python.readthedocs.io/).

How to compile
---------------

You will need to build and install the graphANNIS library (Rust version) with cargo for your system before you can package and install the Python project with `setup.py`.

- Install the latest version (at least 1.31.0) of Rust:
- Clone the graphANNIS library from https://github.com/korpling/graphANNIS/
- Execute `cargo build --release --features "c-api"`  in the cloned repository
- Change to a clone of this graphANNIS Python bindings repository
- Copy the resulting  shared library file `<graphANNIS-repo>/target/release/libgraphannis.so` (`libgraphannis.dylib` under MacOS X and `graphannis.dll` under Windows) to `graphannis/<platform>/` where the platform is one of the following:

| Operating system       | `<platform>`  |
|------------------------|---------------|
| Linux (64 bit)         | linux-x86-64  |
| MacOS X (64 bit)       | darwin-x86-64 |
| Windows (64 bit)       | win32-x86-64  |

- Install you the python packages locally (use Python3) for your current user (remove the `--user` to install it system-wide)
```
python3 setup.py install --user
```

3rd party dependencies
----------------------

- CFFI (http://cffi.readthedocs.org/) MIT License
- networkX (http://networkx.github.io/) BSD License

Author(s)
---------

* Thomas Krause (thomaskrause@posteo.de)

Markers.ai Python client
========================

A data labeling Jupyter widget to be used with Markers.ai

Installation
------------

To install using pip:

    $ pip install markers
    $ jupyter nbextension enable --py --sys-prefix markers


For a development installation (requires npm),

    $ git clone https://github.com/markers_ai/python-client.git
    $ cd markers
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix markers
    $ jupyter nbextension enable --py --sys-prefix markers

Release
-------

1. Bump the version number in markers/_version.py
2. Build the distributions (source and binary wheel):
    $ python setup.py sdist bdist_wheel
3. Upload to PyPI test
    $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
4. After ensuring that works, upload to PyPI prod
    $ twine upload dist/*


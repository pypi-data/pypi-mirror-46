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

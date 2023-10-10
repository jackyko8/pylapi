.. _installation:

Installation of PyLapi
======================

Please follow these instructions to install PyLapi and its generator, replacing all variables accordingly.

To install the PyLapi class:

.. code-block:: bash

    pip install pylapi

To generate a PyLapi supported Python API:

.. code-block:: bash

    pylapi-autogen --template > myapi_config.py
    # Configure myapi_config.py
    pylapi-autogen myapi_config.py
    # Output
    # MyAPI generated and saved in ./myapi.py

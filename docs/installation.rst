.. _installation:

Installation of PyLapi
======================

Please follow these instructions to install PyLapi and its generator, replacing all variables accordingly.

To install the PyLapi class:

.. code-block:: bash

    pip install pylapi

To install the PyLapi generator:

.. code-block:: bash

    cd $PATH_TO_DEV_ENV
    git clone https://github.com/jackyko8/pylapi.git
    cd pylapi
    cp tools/pylapi_gen* $PATH_TO_BIN


To generate a PyLapi supported Python API:

.. code-block:: bash

    cd $PATH_TO_MYAPI
    cp $PATH_TO_DEV_ENV/pylapi/tools/pylapi_config_template.py myapi_config.py
    # Configure myapi_config.py
    pylapi_gen myapi_config.py
    # Output
    # MyAPI generated and saved in ./myapi.py

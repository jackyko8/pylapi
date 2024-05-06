# PyLapi

Python Lightweight API (PyLapi) is a Python API builder. It takes only a few seconds to automatically generate a Python API from OpenAPI specifications or less than an hour for an experienced Python developer to create a custom Python API.

Here is an [overview](./OVERVIEW.md).

## Install PyLapi

Please follow these instructions to install PyLapi and its generator.

To install the PyLapi class:
```bash
pip install pylapi
```

To generate a PyLapi supported Python API:

```bash
pylapi-autogen --template > myapi_config.py
# Configure myapi_config.py
pylapi-autogen myapi_config.py
# Output
# MyAPI generated and saved in ./myapi.py
```

Please replace `myapi_config.py` with the file name you want.

## More Information

PyLapi [tutorial](https://github.com/jackyko8/pylapi/blob/main/tutorials) and [user guide](https://github.com/jackyko8/pylapi/blob/main/user_guide) are available at the [PyLapi](https://github.com/jackyko8/pylapi) GitHub repository.
PyLapi API is documented on [Read the Docs](https://pylapi.readthedocs.io/).

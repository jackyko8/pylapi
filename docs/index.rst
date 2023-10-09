.. pylapi documentation master file, created by
   sphinx-quickstart on Tue Oct 10 08:00:29 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python Lightweight API (PyLapi)
===============================

Python Lightweight API (PyLapi) is a Python API builder. It takes only a few seconds to automatically generate a Python API from OpenAPI specifications or less than an hour for an experienced Python programmer to create a custom Python API.

The auto-generated Python API contains fully functional resource classes with API methods embedded with OpenAPI specifications as inline comments, so you don't need to read the lengthy OpenAPI Specification to study or use the API.

----

You can also manually "rewrite" some of the generated classes and methods in a separate code file, for example, by specifying custom parameters, pre-processing the request, or post-processing the response. The PyLapi generator will merge your code into the generated Python API.

PyLapi's code-rewrite feature allows you to specify different API URLs for individual resources, effectively combining multiple API backend services into a single client API. All parameters and the request body are dynamically mapped based on the API method path, with the option to rewrite them if you so choose.

----

When OpenAPI Specifications are not available or you want to create a Python API your own way, you can inherit your API class from PyLapi, which does all the heavy lifting for you, so your code would mostly be a ``pass``. For example,

.. code-block:: python

   from pylapi import PyLapi

   class MyAPI(PyLapi):
      def __init__(self, *args, **kwargs) -> None:
         super().__init__(*args, **kwargs)
         self.api_url = "https://api.example.com"
         self.api_auth_type = "Bearer"

   # resource_name="invoice", resource_base_path="invoices"
   @MyAPI.resource_class("invoice", "invoices")
   class InvoiceResource(MyAPI):

      @MyAPI.resource_method("{invoice_number}", http_method="GET")
      def getInvoice(self): pass
      # To call: MyAPI.resource("invoice").getInvoice(...)
      # Request: GET https://api.example.com/invoices/{invoice_number}

The ``MyAPI`` API root class inherits the decorators ``@MyAPI.resource_class`` and ``@MyAPI.resource_methods`` from ``PyLapi``, which prepares the API parameters and the request body in the API request, sends the request to the API URL endpoint, processes the response, and handles the resource data for you.


More Information
================

PyLapi `tutorial`_ and `user guide`_ are available at `PyLapi`_ GitHub repository.

.. _tutorial: https://github.com/jackyko8/pylapi/blob/main/tutorials
.. _user guide: https://github.com/jackyko8/pylapi/blob/main/user_guide
.. _PyLapi: https://github.com/jackyko8/pylapi


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   tutorial
   api-reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

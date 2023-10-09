.. _tutorial:

Tutorial
========

Here is a sample PyLapi class:

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

---
The PyLapi framework makes it very easy and natural for you to use a PyLapi-supported Python API. For example,

.. code-block:: python

    from myapi import MyAPI

    MyAPI.auth(AUTH_ACCESS_TOKEN)

    invoice = MyAPI.resource("invoice")
    invoice.data = invoice.getInvoice("12345678") # using positional arguments
    print(invoice)

    item_list = invoice.getItemList()
    product = MyAPI.resource("product")
    invoice_total = 0.0
    for item in item_list:
        product.data.number = item["product_number"]
        product.data = product.getProduct() # using implicit arguments from product.data
        subtotal = product.data.price * item["qty"]
        invoice_total += subtotal
        print(f"Item: {product.data.name}")
        print(f"  Price: ${product.data.price:0.2f}")
        print(f"  Qty: {item['qty']}")
        print(f"  Subtotal: ${subtotal:0.2f}")
    print(f"Invoice Total: ${invoice_total:0.2f}")


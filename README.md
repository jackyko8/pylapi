# PyLapi

Python Lightweight API (PyLapi) is a Python API builder. It takes only a few seconds to automatically generate a Python API from OpenAPI specifications or less than an hour for an experienced Python programmer to create a custom Python API.

The auto-generated Python API contains fully functional resource classes with API methods embedded with OpenAPI specifications as inline comments, so you don't need to read the lengthy OpenAPI Specification to study or use the API.

---
You can also manually "rewrite" some of the generated classes and methods in a separate code file, for example, by specifying custom parameters, pre-processing the request, or post-processing the response. The PyLapi generator will merge your code into the generated Python API.

PyLapi's code-rewrite feature allows you to specify different API URLs for individual resources, effectively combining multiple API backend services into a single client API. All parameters and the request body are dynamically mapped based on the API method path, with the option to rewrite them if you so choose.

---
When OpenAPI Specifications are not available or you want to create a Python API your own way, you can inherit your API class from PyLapi, which does all the heavy lifting for you, so your code would mostly be a `pass`. For example,

```python
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
```

The `MyAPI` API root class inherits the decorators `@MyAPI.resource_class` and `@MyAPI.resource_methods` from `PyLapi`, which prepares the API parameters and the request body in the API request, sends the request to the API URL endpoint, processes the response, and handles the resource data for you.

---
The PyLapi framework makes it very easy and natural for you to use a PyLapi-supported Python API. For example,

```python
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
```

## Install PyLapi

Please follow these instructions to install PyLapi and its generator, replacing all variables accordingly.

To install the PyLapi class:
```bash
pip install pylapi
```

To install the PyLapi generator:

```bash
cd $PATH_TO_DEV_ENV
git clone https://github.com/jackyko8/pylapi.git
cd pylapi
cp tools/pylapi_gen* $PATH_TO_BIN
```

To generate a PyLapi supported Python API:

```bash
cd $PATH_TO_MYAPI
cp $PATH_TO_DEV_ENV/pylapi/tools/pylapi_config_template.py myapi_config.py
# Configure myapi_config.py
pylapi_gen myapi_config.py
# Output
# MyAPI generated and saved in ./myapi.py
```

## More Information

PyLapi [tutorial](https://github.com/jackyko8/pylapi/blob/main/tutorials) and [user guide](https://github.com/jackyko8/pylapi/blob/main/user_guide) are available at [PyLapi](https://github.com/jackyko8/pylapi) GitHub repository.

# PyLapi

Python Lightweight API (PyLapi) is a Python API builder. It takes only a few seconds to automatically generate a Python API from OpenAPI specifications or less than an hour for an experienced Python developer to create a custom Python API.

You can drive PyLapi in an [automatic](./tutorials/2.%20How%20to%20use%20a%20PyLapi%20API.ipynb), [semiautomatic](./tutorials/5.%20PyLapi%20Generator%20Automation.ipynb), or [manual](./tutorials/3.%20A%20ChatGPT%20Conversation%20with%20PyLapi.ipynb) way.

***Automatic***:

The auto-generated Python API contains fully functional resource classes with API methods embedded with OpenAPI specifications as user guide inline comments, so you don't need to read the lengthy OpenAPI Specification to study or use the API.

For more details, please see the [Automatic API Generation](#automatic-api-generation) section and this [tutorial](./tutorials/2.%20How%20to%20use%20a%20PyLapi%20API.ipynb) on how to use the generated API.

***Semiautomatic***:

You can also manually "rewrite" some of the generated classes and methods in a separate code file to, for example, specify custom parameters, pre-process the request, or post-process the response. The PyLapi generator will merge your code into the generated Python API automatically.

PyLapi's code-rewrite feature allows you to specify different API URL endpoints for individual resources, effectively combining multiple API backend services into a single frontend API. All parameters and the request body are dynamically mapped based on the API method route, with the option to rewrite them if you so choose.

More details can be found in this [tutorial](./tutorials/5.%20PyLapi%20Generator%20Automation.ipynb).

***Manual***:

When OpenAPI Specifications are not available or you want to create a Python API your own way, you can inherit your root API class from PyLapi, which does all the heavy lifting for you, so your code would mostly be a `pass`.

If you want to manipulate the API requests and responses, only minimal coding is required. In the tutorial [A ChatGPT Conversation with PyLapi](./tutorials/3.%20A%20ChatGPT%20Conversation%20with%20PyLapi.ipynb), a fully functional Conversation resource is completed in 38 lines, allowing you to do cool things like this:

```python
conversation.ask("Where is the Sydney Opera House?")
print(conversation.data.answers[0])
# Output:
# The Sydney Opera House is located in Sydney, Australia. Specifically, it is situated on Bennelong Point in the Sydney Harbour, close to the Sydney Harbour Bridge.
```

When OpenAPI Specifications are not available or you want to create a Python API your own way, you can inherit your API class from PyLapi, which does all the heavy lifting for you, so your code would mostly be a `pass`. For example,

More details can be found in this [tutorial](./tutorials/3.%20A%20ChatGPT%20Conversation%20with%20PyLapi.ipynb).


## A PyLapi code example

Here is a sample of a PyLapi API:

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

To generate a PyLapi supported Python API:

```bash
pylapi-autogen --template > myapi_config.py
# Configure myapi_config.py
pylapi-autogen myapi_config.py
# Output
# MyAPI generated and saved in ./myapi.py
```

## More Information

PyLapi [tutorial](https://github.com/jackyko8/pylapi/blob/main/tutorials) and [user guide](https://github.com/jackyko8/pylapi/blob/main/user_guide) are available at [PyLapi](https://github.com/jackyko8/pylapi) GitHub repository.

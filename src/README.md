# PyLapi

Python Lightweight API (PyLapi) is a Python API builder. It takes only a few seconds to automatically generate a Python API from OpenAPI specifications or less than an hour for an experienced Python programmer to create a custom one.

To install PyLapi:
```bash
pip install pylapi
```

## Automatic API Generation

The auto-generated Python API contains fully functional resource classes with API methods embedded with OpenAPI specifications as inline comments, so you don't need to read the lengthy OpenAPI JSON or YAML document to use the API.

```bash
git clone https://github.com/jackyko8/pylapi.git
cd pylapi
cp tools/pylapi_gen* /path/to/bin
cp tools/pylapi_config_template.py /path/to/myapi/myapi_config.py
cd /path/to/myapi
# Customise myapi_config.py (as shown next)
pylapi_gen myapi_config.py
# Output
# MyAPI generated and saved in ./myapi.py
```

Typical `myapi_config.py`
```python
oas_file_name = "./myapi_oas.json"
output_py_name = "./myapi.py"
api_class_name = "MyAPI"
guide_attrs = {
    "summary",
    "description",
    "parameters",
    "request_body",
    # "ref",
}
naming = {
    "class_name": "upperCamel($.path_items[0]) + 'Resource'",
    "resource_name": "snake($.path_items[0])",
    "class_path": "$.path_items[0]",
    "resource_path": "'/'.join($.path_items[1:])",
    "method_name": "lowerCamel($.operation_id)",
}
```

Example use:
```python
from myapi import MyAPI

MyAPI.auth(AUTH_ACCESS_TOKEN)

invoice = MyAPI.resource("invoice")
invoice.getInvoice("12345678")
print(invoice)

item_list = invoice.getItemList()
product = MyAPI.resource("product")
for item in item_list:
    product.number = item["product_number"]
    product.getProduct()
    print(f"Item: {product.data.name}")
    print(f"  Price: ${product.data.price}")
    print(f"  Qty: ${item['qty']}")
    print(f"  Total: ${product.data.price * item['qty']")
```

## Semi-automatic Code Rewrite

You can also manually "rewrite" some of the generated classes or methods in a separate file, e.g., by specifying custom parameters, pre-processing the request, or post-processing the response. The generator will merge your code into the generated API.

File: `myapi_rewrite.py`
```python
@oAPI.resource_class("chat", "chat")
class ChatResource(oAPI):
    ...

    @oAPI.resource_method("completions", "POST", load="$")
    def talk(self, question: str):
        default_model = "gpt-3.5-turbo"
        ...

        @oAPI.callback
        def request(self, **kwargs):
            ...

        @oAPI.callback
        def response(self, **kwargs):
            ...
```

File: `myapi_config.py`
```python
...
code_rewrite_file_name = "./myapi_rewrite.py"
...
```

Regenerate the Python API:
```bash
pylapi_gen myapi_config.py
# Output
# MyAPI generated, merged with ./myapi_rewrite.py, and saved in ./myapi.py
```

## Manual API Build

When OpenAPI specifications are not available or you want to create a Python API your own way, you can inherit from the PyLapi class and build API methods using decorators like `@MyAPI.resource_class` and `@MyAPI.resource_methods`. The API parameters and the request body will be taken care of by PyLapi.

The "rewrite" feature also allows you to specify different API URLs for individual resources, effectively combining multiple APIs into a single framework. All parameters and the request body are dynamically mapped based on the API method route.

File `myapi_rewrite.py`
```python
@MyAPI.resource_class("invoice", "invoices")
class InvoiceResource(aAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.api_url = "https://invoice.example.com/api/1.0"

@MyAPI.resource_class("product", "products")
class ProductResource(aAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.api_url = "https://product.example.com/api/1.0"
```

In the above example, the `InvoiceResource` and `ProductResource` are services provided by two different API URLs.

## More Information

PyLapi [tutorial](https://github.com/jackyko8/pylapi/blob/main/tutorials) and [user guide](https://github.com/jackyko8/pylapi/blob/main/user_guide) are available at [PyLapi](https://github.com/jackyko8/pylapi) GitHub repository.

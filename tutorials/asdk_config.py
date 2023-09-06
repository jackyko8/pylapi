# aSDK Generator Configuration

# The OpenAPI specifiation file in JSON or YAML
oas_file_name = "./asana_oas.yaml"
output_py_name = "./asdk.py"

# The authentication type prepended to the access credential
api_auth_type = "Bearer"

# The API Server URL
# Default oas.server[0].url
# api_url = "https://api.example.com"

# The PyLapi API class name (the comment parent of all Resource classes)
# Default oas.info.title
api_class_name = "aSDK"

# Naming of resource classes, names, paths, and methods
# Available magic words conversions:
#   snake
#   kebab
#   pascal (upperCamel)
#   camel (lowerCamel)
#   singular
naming = {
    # Resource Class Name:
    # class ExampleResource(...):
    # Example: UpperCamel case plus "Resource" for class names
    "class_name": "upperCamel(singular($.path_items[0])) + 'Resource'",

    # Resource Name used to create a resource object:
    # my_resource = MyAPI.resource("example_resource")
    # Example: Snake case for resource names
    "resource_name": "snake(singular($.path_items[0]))",

    # API path prefix for all methods in the class
    # API full path is {class_path}/{resource_path}
    # Example: resources as in /resources/api_method/...
    # IMPORTANT: Make sure the class_path is common to all methods in the class.
    "class_path": "$.path_items[0]",

    # API path suffix for the method
    # API full path is {class_path}/{resource_path}
    # Example: api_method as in /resources/api_method/...
    "resource_path": "re.sub(r'{[a-zA-Z0-9_-]+gid}', '{gid}', '/'.join($.path_items[1:]))",

    # Method Name
    # def exampleMethod(self):
    # Example: Lower Camel case for method names
    "method_name": "lowerCamel($.operation_id)",
}

# Optional guide of OpenAPI method specifications; can be overwritten from CLI
# Please comment out unwanted ones
guide_attrs = {
    "summary",
    "description",
    "parameters",
    "request_body",
    # "ref",
}

# Optional Python statements appended to the standard API class __init__()
# Please start the statements on the left without extra indentation.
api_class_init = """
self._resource_attrs.update({"gid": "$.gid"})
"""

# Optional methods in the API class (to be inherited by all resource classes)
# Please start the statements on the left without extra indentation.
api_methods = """
@PyLapi.resource_method(give="$.data")
def _list(self): pass

@PyLapi.resource_method("{gid}", give="$.data", load="$.data")
def _load(self): pass

@PyLapi.resource_method(http_method="POST", give="$.data", load="$.data", send={"data": "$"})
def _create(self): pass

@PyLapi.resource_method("{gid}", http_method="PUT", give="$.data", load="$.data", send={"data": "$"})
def _update(self): pass

@PyLapi.resource_method("{gid}", http_method="DELETE", give=None)
def _delete(self): pass
"""

# Optional resource_method decorator arguments (applied to all resource methods in the SDK)
# For example, {"send": {"data": "$"}, "give": "$.data"}
resource_method_args = {"send": {"data": "$"}, "give": "$.data"}

# GhSDK Generator Configuration

# The OpenAPI specifiation file in JSON
oas_file_name = "./api.github.com.json"
output_py_name = "./ghsdk.py"

# The authentication type prepended to the access credential
api_auth_type = "Bearer"

# The API Server URL
# Default oas.server[0].url
# api_url = "https://api.example.com"

# The PyLapi API class name (the comment parent of all Resource classes)
# Default oas.info.title
api_class_name = "GhSDK"

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
    "class_path": "''",

    # API path suffix for the method
    # API full path is {class_path}/{resource_path}
    # Example: api_method as in /resources/api_method/...
    "resource_path": "'/'.join($.path_items)",

    # Method Name
    # def exampleMethod(self):
    # Example: Lower Camel case for method names
    "method_name": "lowerCamel($.operation_id)",
}

# Optional Python statements appended to the standard API class __init__()
# Please start the statements on the left without extra indentation.
# api_class_init = """
# """

# Optional methods in the API class (to be inherited by all resource classes)
# Please start the statements on the left without extra indentation.
# api_methods = """
# """

# Optional guide of OpenAPI method specifications; can be overwritten from CLI
# Please comment out unwanted ones
guide_attrs = {
    "summary",
    "description",
    "parameters",
    "request_body",
    # "ref",
}

# Optional resource_method decorator arguments (applied to all resource methods in the SDK)
# For example, {"send": {"data": "$"}, "give": "$.data"}
# resource_method_args = {}

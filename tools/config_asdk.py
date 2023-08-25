# GhSDK Generator Configuration
import re

# The OpenAPI specifiation file in JSON
oas = "./alpha/asana/asana_oas.json"

# The authentication type prepended to the access credential
api_auth_type = "Bearer"

# The PyLapi SDK class name (the comment parent of all Resource classes)
sdk_class_name = "aSDK"

# Optional Python statements appended to the standard SDK class __init__()
# Please start the statements on the left without extra indentation.
sdk_class_init = """
self._resource_ids.update({"gid": "$.gid"})
"""

# Optional methods in the SDK class (to be inherited by all resource classes)
# Please start the statements on the left without extra indentation.
sdk_methods = """
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

# Optional resource_method decorator arguments
# For example, {"send": {"data": "$"}, "give": "$.data"}
resource_method_args = {"send": {"data": "$"}, "give": "$.data"}


# For naming conversion, use MagicWords(name).<conversion>, where <conversion> can be
# snake, kebab, pascal (upperCamel), camel (lowerCamel), or singular
# e.g., MagicWords("ThisIs a good_test for magic-words_conversion.").snake
#       Output: this_is_a_good_test_for_magic_words_conversion
from pylapi import MagicWords


class Method():
    def __init__(self, method):
        self._method = method
        self._path_items = self._method["path"].split("/")

    def __repr__(self):
        return str(self._method)

    @property
    def api_path(self):
        _api_path = "/" + self.class_path if self.class_path else ""
        _api_path += "/" + self.resource_path if self.resource_path else ""
        return _api_path

    ########################################
    #
    # Derived attributes - customisables
    #   These attributes are derived from the original
    #   OpenAPI JSON attributes in the next section.
    #

    # Resource Class Name:
    # class ExampleResource(...):
    # Example: UpperCamel case plus "Resource" for class names
    @property
    def class_name(self):
        return MagicWords(MagicWords(self._path_items[0]).singular).upperCamel + "Resource"

    # Resource Name used to create a resource object:
    # my_resource = MySDK.resource("example_resource")
    # Example: Snake case for resource names
    @property
    def resource_name(self):
        return MagicWords(MagicWords(self._path_items[0]).singular).snake

    # API path prefix for all methods in the class
    # API full path is {class_path}/{resource_path}
    # Example: resources in /resources/api_method/...
    # IMPORTANT: Make sure the class_path is common to all methods in the class.
    @property
    def class_path(self):
        return self._path_items[0]

    # API path suffix for the method
    # API full path is {class_path}/{resource_path}
    # Example: api_method in /resources/api_method/...
    @property
    def resource_path(self):
        return re.sub(r"{[a-zA-Z0-9_-]+gid}", "{gid}", "/".join(self._path_items[1:]))

    # Method Name
    # def exampleMethod(self):
    # Example: Lower Camel case for method names
    @property
    def method_name(self):
        return MagicWords(self.operation_id).lowerCamel


    ########################################
    #
    # Initialised attributes - not to be customised
    #   These attributes are captured from the
    #   OpenAPI JSON file, and returned without
    #   conversion (except http_method to uppercase).
    #
    @property
    def path(self):
        return self._method["path"]

    @property
    def http_method(self):
        return self._method["http_method"].upper()

    @property
    def operation_id(self):
        return self._method["operation_id"]

    # The followings are used for documentation in the generated file.
    # Comment out, or return blank, None, or False to suppress.
    @property
    def summary(self):
        return self._method["summary"]

    @property
    def description(self):
        return self._method["description"]

    @property
    def parameters(self):
        return self._method["parameters"]
